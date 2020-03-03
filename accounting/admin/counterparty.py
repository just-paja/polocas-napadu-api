from admin_auto_filters.filters import AutocompleteFilter

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _

from fields.admin import BaseAdminModel, BaseStackedAdminModel

from ..models import CounterParty, KnownAccount, Statement


def pair_known_account_to_statements(account):
    statements = Statement.objects.filter(counterparty__isnull=True)
    for statement in statements:
        if account.matches_statement(statement):
            statement.counterparty = account.owner
            statement.save()


class KnownAccountInlineAdmin(BaseStackedAdminModel):
    model = KnownAccount
    extra = 0


class CounterPartyAdmin(BaseAdminModel):
    model = CounterParty
    inlines = [KnownAccountInlineAdmin]
    list_display = ('name', 'count_accounts', 'count_statements', 'created', 'modified')
    change_form_template = 'admin/counterparty_change_form.html'
    change_list_template = 'admin/counterparty_change_list.html'
    search_fields = (
        'name',
        'accounts__sender_account_number',
        'accounts__sender_bank',
        'accounts__sender_iban',
        'accounts__sender_bic',
    )
    ordering = ('-modified',)

    def get_urls(self):
        return super().get_urls() + [
            path(
                'pair',
                self.admin_site.admin_view(self.pair_all),
                name='counterparty_pair_all'
            ),
            path(
                '/<counterparty_id>/pair',
                self.admin_site.admin_view(self.pair_counterparty),
                name='counterparty_pair'
            ),
        ]

    def pair_counterparty_to_statements(self, counterparty):
        for account in counterparty.accounts.all():
            pair_known_account_to_statements(account)

    def pair_counterparty(self, request, counterparty_id):
        counterparty = get_object_or_404(CounterParty, pk=counterparty_id)
        self.pair_counterparty_to_statements(counterparty)
        messages.add_message(request, messages.SUCCESS, _('Pairing was finished'))
        return redirect(reverse(
            'accounting:accounting_counterparty_change',
            args=[counterparty.pk]
        ))

    def pair_all(self, request):
        for counterparty in CounterParty.objects.all():
            self.pair_counterparty_to_statements(counterparty)
        messages.add_message(request, messages.SUCCESS, _('Pairing was finished'))
        return redirect(reverse('accounting:accounting_counterparty_changelist'))

    def get_queryset(self, request):
        querystring = super().get_queryset(request)
        querystring = querystring.annotate(Count('statements', distinct=True))
        querystring = querystring.annotate(Count('accounts', distinct=True))
        return querystring

    def count_accounts(self, obj):
        return obj.accounts__count

    def count_statements(self, obj):
        return obj.statements__count

    count_accounts.short_description = _('Known accounts')
    count_accounts.admin_order_field = 'accounts__count'
    count_statements.short_description = _('Statements')
    count_statements.admin_order_field = 'statements__count'


class KnownAccountAdmin(BaseAdminModel):
    model = KnownAccount
    fields = (
        'owner',
        'sender_account_number',
        'sender_bank',
        'sender_iban',
        'sender_bic',
    )
    list_display = (
        'sender_account_number',
        'sender_bank',
        'sender_iban',
        'sender_bic',
        'owner',
        'created',
        'modified'
    )
    change_form_template = 'admin/known_account_change_form.html'
    search_fields = ('sender_account_number', 'sender_bank', 'sender_iban', 'sender_bic')

    def get_urls(self):
        return super().get_urls() + [
            path(
                '<known_account_id>/pair',
                self.admin_site.admin_view(self.pair_known_account),
                name='known_account_pair'
            ),
        ]

    def pair_known_account(self, request, known_account_id):
        pair_known_account_to_statements(get_object_or_404(KnownAccount, pk=known_account_id))
        return redirect(reverse(
            'accounting:accounting_knownaccount_change',
            args=[known_account_id]
        ))


class CounterPartyFilter(AutocompleteFilter):
    title = _("Counterparty")
    field_name = "counterparty"
