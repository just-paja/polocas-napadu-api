import datetime
import pytest

from django.test import TestCase
from graphene.test import Client
from model_bakery import baker

from ..counter_party import CounterParty, KnownAccount
from ..statement import Statement

class StatementTest(TestCase):
    def test_pairs_counter_party_based_on_account_number(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank account',
        )
        owner = baker.make(
            'accounting.CounterParty',
            name='Test counter party',
        )
        known_account = baker.make(
            'accounting.KnownAccount',
            owner=owner,
            sender_bank='2010',
            sender_account_number='336699111',
        )
        statement = baker.make(
            'accounting.Statement',
            account=account,
            sender_bank='2010',
            sender_account_number='336699111',
        )
        assert statement.known_account == known_account

    def test_pairs_counter_party_based_on_iban(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank account',
        )
        owner = baker.make(
            'accounting.CounterParty',
            name='Test counter party',
        )
        known_account = baker.make(
            'accounting.KnownAccount',
            owner=owner,
            sender_iban='CZ0920100000001234567892',
        )
        statement = baker.make(
            'accounting.Statement',
            account=account,
            sender_iban='CZ0920100000001234567892',
        )
        assert statement.known_account == known_account

    def test_pairs_promise_based_on_variable_symbol(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank account',
        )
        promise = baker.make(
            'accounting.Promise',
            variable_symbol='232323',
        )
        statement = baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='232323',
        )
        assert statement.promise == promise

    def test_pairs_promise_based_on_variable_and_specific_symbol(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank account',
        )
        promise2 = baker.make(
            'accounting.Promise',
            variable_symbol='232323',
            specific_symbol='2',
        )
        statement = baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='232323',
            specific_symbol='2',
        )
        assert statement.promise == promise2
