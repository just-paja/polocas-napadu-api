import datetime
import pytest

from freezegun import freeze_time
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from dateutil.parser import parse
from model_bakery import baker
from unittest import mock

import fiobank

from ..bank_sync import sync_fio
from ..models import BankScrape

def scrape_repr(promise):
    return {
        'account': promise.account,
        'days_back': promise.days_back,
        'source': promise.source,
        'status': promise.status,
    }

def statement_repr(statement):
    return {
        'account': statement.account,
        'amount': statement.amount,
        'ident': statement.ident,
        'counterparty': statement.counterparty,
        'message': statement.message,
        'promise': statement.promise,
        'scrape': statement.scrape,
        'user_identification': statement.user_identification,
    }

def scrape_with_a_statement(*args):
    return [
        {
            'account_number': '23123123',
            'amount': 300,
            'bank_code': '0300',
            'constant_symbol': None,
            'currency': 'CZK',
            'date': parse('2020-02-01').date(),
            'recipient_message': '',
            'specific_symbol': None,
            'transaction_id': 42,
            'user_identification': 'xxx',
            'variable_symbol': '393939',
        }
    ]

class BankSyncTest(TestCase):
    @mock.patch.object(fiobank.FioBank, 'period')
    def test_sync_fio_creates_scrape(self, FioBank):
        account = baker.make(
            'accounting.Account',
            currency='CZK',
            description='Test account',
            name='Test account',
        )
        sync_fio(account, 10)
        self.assertQuerysetEqual(account.scrapes.all(), [
            {
                'account': account,
                'days_back': 10,
                'source': 1,
                'status': 2,
            }
        ], scrape_repr)

    @mock.patch.object(fiobank.FioBank, 'period', scrape_with_a_statement)
    def test_sync_fio_creates_statements(self):
        account = baker.make(
            'accounting.Account',
            currency='CZK',
            description='Test account',
            name='Test account',
        )
        sync_fio(account, 10)
        self.assertQuerysetEqual(account.scrapes.first().statements.all(), [
            {
                'account': account,
                'scrape': account.scrapes.first(),
                'amount': 300,
                'message': '',
                'promise': None,
                'ident': '42',
                'counterparty': None,
                'user_identification': 'xxx',
            }
        ], statement_repr)
