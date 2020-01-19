from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .bank_sync import sync_fio
from .models import Account


@staff_member_required
def bank_sync(request):
    pass


@staff_member_required
def account_bank_sync(request, account_id):
    account = get_object_or_404(Account, pk=account_id, fio_readonly_key__isnull=False)
    five_years_back = 1825
    sync_fio(account, five_years_back)
    return redirect(reverse('admin:accounting_statement'))
