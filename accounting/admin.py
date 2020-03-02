from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.admin.filters import SimpleListFilter
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from fields.admin import BaseAdminModel, BaseStackedAdminModel, BaseInlineAdminModel

from .models import (
    Account,
    CounterParty,
    Debt,
    KnownAccount,
    Membership,
    MembershipFee,
    MembershipLevel,
    MembershipLevelFee,
    Promise,
    Purpose,
    PurposeCategory,
    Statement,
)

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


class AccountAdmin(BaseAdminModel):
    model = Account
    fields = (
        'name',
        'description',
        'currency',
        'account_number',
        'bank',
        'iban',
        'bic',
        'fio_readonly_key',
        'visibility'
    )
    list_display = ('name', 'currency', 'get_ballance', 'iban', 'visibility', 'modified')
    search_fields = ('name', 'description', 'account_number', 'bank', 'iban', 'bic')
    list_filter = ('currency', 'visibility')
    change_form_template = 'admin/account_change_form.html'
    change_list_template = 'admin/account_change_list.html'


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


class DebtAdmin(BaseInlineAdminModel):
    model = Debt
    fields = ('amount', 'currency', 'maturity')
    extra = 0


class PurposeFilter(AutocompleteFilter):
    title = _("Purpose")
    field_name = "purpose"


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
        'modified'
    )
    search_fields = (
        'variable_symbol',
        'specific_symbol',
        'constant_symbol',
        'name',
    )


class MembershipLevelFeeAdmin(BaseInlineAdminModel):
    model = MembershipLevelFee
    fields = ('amount', 'currency', 'start', 'end')
    extra = 0


class MembershipLevelAdmin(BaseAdminModel):
    model = MembershipLevel
    search_fields = ('name', 'description')
    list_display = ('name', 'is_active', 'start', 'end', 'modified')
    inlines = (MembershipLevelFeeAdmin,)
    fields = ('name', 'description', 'start', 'end')


class MembershipFeeAdmin(BaseInlineAdminModel):
    model = MembershipFee
    fieldsets = (
        (None, {
            'fields': ('level_fee', 'start', 'end'),
        }),
    )
    list_display = (
        'name',
        'amount',
        'get_volume_price_tag',
        'modified'
    )
    search_fields = (
        'membership__user__first_name',
        'membership__user__last_name',
        'purpose__name'
    )
    autocomplete_fields = ('membership',)


class MembershipAdmin(BaseAdminModel):
    model = Membership
    search_fields = ('user__first_name', 'user__last_name')
    autocomplete_fields = ('user',)
    list_display = ('user', 'level', 'is_active', 'start', 'end', 'modified')
    fields = ('user', 'level', 'start', 'end')


class AccountFilter(AutocompleteFilter):
    title = _("Account")
    field_name = "account"


class PromiseFilter(AutocompleteFilter):
    title = _("Promise")
    field_name = "promise"


class CounterPartyFilter(AutocompleteFilter):
    title = _("Counterparty")
    field_name = "counterparty"


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
            link = reverse('admin:accounting_counterparty_change', args=[owner.pk])
            return format_html('<a href="%s">%s</a>' % (link, name))
        return None

    link_counterparty.short_description = _('Counterparty')
    link_counterparty.admin_order_field = 'counterparty__name'


class PurposeAdmin(BaseAdminModel):
    model = Purpose
    fields = ('name', 'description')
    list_display = (
        'id',
        'name',
        'get_promise_count',
    )
    list_filter = ()
    search_fields = ('name', 'description')


class PurposeCategoryAdmin(BaseAdminModel):
    model = PurposeCategory
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'purposes'),
        }),
    )
    list_display = (
        'id',
        'name',
    )
    list_filter = ()
