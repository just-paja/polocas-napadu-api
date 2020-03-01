from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .bank_sync import sync_fio
from .models import Account, CounterParty, KnownAccount, Statement


@staff_member_required
def bank_sync(request):
    pass


def pair_known_account_to_statements(account):
    statements = Statement.objects.filter(known_account__isnull=True)
    for statement in statements:
        if account.matches_statement(statement):
            statement.known_account = account
            statement.save()


@staff_member_required
def counterparty_pair(request, counterparty_id):
    counterparty = get_object_or_404(CounterParty, pk=counterparty_id)
    for account in counterparty.accounts.all():
        pair_known_account_to_statements(account)
    return redirect(reverse('admin:accounting_counterparty_change', args=[counterparty.pk]))


@staff_member_required
def known_account_pair(request, known_account_id):
    pair_known_account_to_statements(get_object_or_404(KnownAccount, pk=known_account_id))
    return redirect(reverse('admin:accounting_knownaccount_change', args=[known_account_id]))


@staff_member_required
def account_bank_sync(request, account_id):
    account = get_object_or_404(Account, pk=account_id, fio_readonly_key__isnull=False)
    five_years_back = 1825
    sync_fio(account, five_years_back)
    return redirect(reverse('admin:accounting_statement_changelist'))
