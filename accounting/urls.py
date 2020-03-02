from django.urls import path

from .views import (
    account_bank_sync,
    bank_sync,
    counterparty_pair,
    known_account_pair,
    promises_regenerate_recurrency,
)

urlpatterns = [  # pylint:disable=invalid-name
    path('account/<account_id>/bank-sync', account_bank_sync, name='bank_sync_account'),
    path('account/bank-sync', bank_sync, name='bank_sync'),
    path('counterparty/<counterparty_id>/pair', counterparty_pair, name='counterparty_pair'),
    path('known-account/<known_account_id>/pair', known_account_pair, name='known_account_pair'),
    path(
        'promises/regenerate-recurrency',
        promises_regenerate_recurrency,
        name='promises_regenerate_recurrency'
    ),
]
