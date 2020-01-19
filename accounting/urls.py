from django.urls import path

from .views import bank_sync, account_bank_sync

urlpatterns = [  # pylint:disable=invalid-name
    path('account/bank-sync', bank_sync, name='bank_sync'),
    path('account/<account_id>/bank-sync', account_bank_sync, name='bank_sync_account'),
]
