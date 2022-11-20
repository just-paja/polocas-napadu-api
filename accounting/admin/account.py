from admin_auto_filters.filters import AutocompleteFilter

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from fields.admin import BaseAdminModel

from ..models import Account
from ..bank_sync import sync_fio


class AccountFilter(AutocompleteFilter):
    title = _("Account")
    field_name = "account"


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

    def get_urls(self):
        return super().get_urls() + [
            path(
                'bank-sync',
                self.admin_site.admin_view(self.bank_sync),
                name='account_bank_sync_all'
            ),
            path(
                '<account_id>/bank-sync',
                self.admin_site.admin_view(self.bank_sync_account),
                name='account_bank_sync'
            ),
        ]

    def sync_account(self, account):
        five_years_back = 1825
        sync_fio(account, five_years_back)

    def bank_sync(self, request):
        accounts = Account.objects.filter(fio_readonly_key__isnull=False).all()
        for account in accounts:
            self.sync_account(account)
        messages.add_message(request, messages.SUCCESS, _('Pairing was finished'))
        return redirect(reverse('accounting:accounting_account_changelist'))

    def bank_sync_account(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id, fio_readonly_key__isnull=False)
        self.sync_account(account)
        messages.add_message(request, messages.SUCCESS, _('Pairing was finished'))
        return redirect(reverse('accounting:accounting_statement_changelist'))
