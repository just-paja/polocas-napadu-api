from admin_auto_filters.filters import AutocompleteFilter

from django.contrib import messages
from django.contrib.admin.filters import SimpleListFilter
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .account import AccountFilter
from .counterparty import CounterPartyFilter
from .purpose import PurposeFilter
from ..models import Debt, KnownAccount, Promise, Statement

DIRECTION_INBOUND = 1
DIRECTION_OUBOUND = 2

DIRECTION_CHOICES = (
    (DIRECTION_INBOUND, _('Inbound')),
    (DIRECTION_OUBOUND, _('Outbound')),
)

PAIR_YES = 1
PAIR_NO = 2

PAIR_CHOICES = (
    (PAIR_YES, _('Yes')),
    (PAIR_NO, _('No')),
)


class PaymentDirectionFilter(SimpleListFilter):
    title = _('Payment direction')
    parameter_name = 'direction'

    def lookups(self, request, model_admin):
        return DIRECTION_CHOICES

    def queryset(self, request, queryset):
        try:
            filter_value = int(self.value())
        except TypeError:
            filter_value = None
        if filter_value == DIRECTION_INBOUND:
            return queryset.filter(amount__gt=0)
        if filter_value == DIRECTION_OUBOUND:
            return queryset.filter(amount__lt=0)
        return queryset


class PaymentPairingStatusFilter(SimpleListFilter):
    title = _('Has pair')
    parameter_name = 'has_pair'

    def lookups(self, request, model_admin):
        return PAIR_CHOICES

    def queryset(self, request, queryset):
        try:
            filter_value = int(self.value())
        except TypeError:
            return queryset
        if filter_value == 1:
            return queryset.filter(promise__isnull=False)
        if filter_value == 2:
            return queryset.filter(promise__isnull=True)
        return queryset


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


class DebtAdmin(BaseInlineAdminModel):
    model = Debt
    fields = ('amount', 'currency', 'maturity')
    extra = 0


class PromiseAdmin(BaseAdminModel):
    class Media:
        pass

    model = Promise
    inlines = [DebtAdmin]
    fieldsets = (
        (None, {
            'fields': ('purpose', 'name'),
        }),
        (None, {
            'fields': ('start', 'repeat', 'end'),
        }),
        (None, {
            'fields': (
                'variable_symbol',
                'specific_symbol',
                'constant_symbol',
            ),
        }),
        (None, {
            'fields': (
                'created',
                'modified',
            ),
        }),
    )
    change_form_template = 'admin/promise_change_form.html'
    change_list_template = 'admin/promise_change_list.html'
    list_filter = (
        'status',
        'repeat',
        PurposeFilter,
        PaymentDirectionFilter,
    )
    list_display = (
        '__str__',
        'purpose',
        'status',
        'amount',
        'get_volume_price_tag',
        'variable_symbol',
        'start',
        'end',
    )
    search_fields = (
        'variable_symbol',
        'specific_symbol',
        'constant_symbol',
        'name',
    )
    readonly_fields = ('created', 'modified')

    def get_urls(self):
        return super().get_urls() + [
            path(
                'regenerate',
                self.admin_site.admin_view(self.promises_regenerate),
                name='promises_regenerate'
            ),
        ]

    def promises_regenerate(self, request):
        promises = Promise.objects.filter(repeat__isnull=False).all()
        for promise in promises:
            promise.save()
        messages.add_message(request, messages.SUCCESS, _('Promise regeneration was finished'))
        return redirect(reverse('accounting:accounting_promise_changelist'))


class PromiseFilter(AutocompleteFilter):
    title = _("Promise")
    field_name = "promise"


class StatementAdmin(BaseAdminModel):
    class Media:
        pass

    model = Statement
    change_form_template = 'admin/statement_change_form.html'
    fieldsets = (
        (None, {
            'fields': ('account',),
        }),
        (None, {
            'fields': (
                'amount',
                'currency',
                'received_at',
                'promise',
            ),
        }),
        (None, {
            'fields': (
                'sender_account_number',
                'sender_bank',
                'sender_iban',
                'sender_bic',
            ),
        }),
        (None, {
            'fields': (
                'variable_symbol',
                'specific_symbol',
                'constant_symbol',
            ),
        }),
        (None, {
            'fields': (
                'ident',
                'user_identification',
                'message',
                'counterparty',
            ),
        }),
    )
    list_display = (
        'id',
        'link_counterparty',
        'amount',
        'promise',
        'received_at',
        'sender_account_number',
        'sender_bank',
        'variable_symbol',
        'specific_symbol',
        'constant_symbol',
    )
    list_filter = (
        PaymentDirectionFilter,
        PaymentPairingStatusFilter,
        AccountFilter,
        PromiseFilter,
        CounterPartyFilter,
    )
    autocomplete_fields = ('promise', 'counterparty')
    search_fields = (
        'promise__name',
        'counterparty__name',
        'variable_symbol',
        'specific_symbol',
        'constant_symbol',
    )

    def link_counterparty(self, statement):
        if statement.counterparty:
            owner = statement.counterparty
            name = owner.name
            link = reverse('accounting:accounting_counterparty_change', args=[owner.pk])
            return format_html('<a href="%s">%s</a>' % (link, name))
        return None

    link_counterparty.short_description = _('Counterparty')
    link_counterparty.admin_order_field = 'counterparty__name'
