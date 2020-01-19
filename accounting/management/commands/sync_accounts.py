#!/usr/bin/env python
from django.core.management.base import BaseCommand

from ...bank_sync import sync_fio
from ...models import Account


class Command(BaseCommand):
    help = 'Reads bank account statements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days-back',
            default=7,
            type=int,
            nargs="?",
            help='Days back, for which will be the statement fetched',
        )

    def handle(self, *args, **kwargs):
        accounts = Account.objects.filter(fio_readonly_key__isnull=False)
        for account in accounts:
            self.read_account(account, kwargs.get('days_back', 7))

    def read_account(self, account, days_back):
        sync_fio(account, days_back)
