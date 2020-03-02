from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .bank_sync import sync_fio
from .models import Account, CounterParty, KnownAccount, Promise, Statement


def pair_known_account_to_statements(account):
    statements = Statement.objects.filter(counterparty__isnull=True)
    for statement in statements:
        if account.matches_statement(statement):
            statement.counterparty = account.owner
            statement.save()

def pair_counterparty_to_statements(counterparty):
    for account in counterparty.accounts.all():
        pair_known_account_to_statements(account)


def sync_account(account):
    five_years_back = 1825
    sync_fio(account, five_years_back)


@staff_member_required
def counterparty_pair(request, counterparty_id):
    counterparty = get_object_or_404(CounterParty, pk=counterparty_id)
    pair_counterparty_to_statements(counterparty)
    return redirect(reverse('admin:accounting_counterparty_change', args=[counterparty.pk]))


@staff_member_required
def counterparty_pair_all(request):
    for counterparty in CounterParty.objects.all():
        pair_counterparty_to_statements(counterparty)
    return redirect(reverse('admin:accounting_counterparty_changelist'))


@staff_member_required
def known_account_pair(request, known_account_id):
    pair_known_account_to_statements(get_object_or_404(KnownAccount, pk=known_account_id))
    return redirect(reverse('admin:accounting_knownaccount_change', args=[known_account_id]))


@staff_member_required
def account_bank_sync(request, account_id):
    account = get_object_or_404(Account, pk=account_id, fio_readonly_key__isnull=False)
    sync_account(account)
    return redirect(reverse('admin:accounting_statement_changelist'))


@staff_member_required
def bank_sync(request):
    accounts = Account.objects.filter(fio_readonly_key__isnull=False).all()
    for account in accounts:
        sync_account(account)
    return redirect(reverse('admin:accounting_account_changelist'))


@staff_member_required
def promises_regenerate_recurrency(request):
    promises = Promise.objects.filter(repeat__isnull=False).all()
    for promise in promises:
        promise.save()
    return redirect(reverse('admin:accounting_promise_changelist'))
