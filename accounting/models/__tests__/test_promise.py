import datetime
import pytest

from freezegun import freeze_time
from django.db.utils import IntegrityError
from django.test import TestCase
from dateutil.parser import parse
from model_bakery import baker

from ..promise import (
    DEBT_SOURCE_GENERATED_INITIAL,
    DEBT_SOURCE_GENERATED_RECURRING,
    DEBT_SOURCE_MANUAL,
    RECURRENCE_MONTHLY,
    STATUS_EXPECTED,
    STATUS_OVERPAID,
    STATUS_PAID,
    STATUS_UNDERPAID
)

def debt_repr(item):
    return {
        'amount': item.amount,
        'maturity': item.maturity,
        'promise': item.promise,
        'source': item.source,
    }

class PromiseTest(TestCase):
    def assert_equal_debts(self, actual, expected):
        return self.assertQuerysetEqual(actual, expected, debt_repr)

    def test_represents_by_name_if_given(self):
        promise1 = baker.make(
            'accounting.Promise',
            name='Member fee',
            variable_symbol='234'
        )
        assert str(promise1) == 'Member fee'

    def test_represents_by_id_given_name_is_none(self):
        promise1 = baker.make(
            'accounting.Promise',
            variable_symbol='234'
        )
        assert str(promise1) == 'Promise#1'

    def test_clean_blocks_clashing_non_recurring_variable_symbols(self):
        baker.make(
            'accounting.Promise',
            variable_symbol='234'
        )
        with pytest.raises(IntegrityError):
            baker.make(
                'accounting.Promise',
                variable_symbol='234'
            )

    def test_save_updates_status_to_expected(self):
        promise1 = baker.make(
            'accounting.Promise',
        )
        assert promise1.status == STATUS_EXPECTED

    def test_save_updates_status_to_paid_given_one_payment_fulfills_it(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank sync',
        )
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333'
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=300,
        )
        promise1.refresh_from_db()
        assert promise1.status == STATUS_PAID

    def test_save_updates_status_to_paid_given_two_payments_fulfill_it(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank sync',
        )
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333'
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=200,
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=100,
        )
        promise1.refresh_from_db()
        assert promise1.status == STATUS_PAID

    def test_save_updates_status_to_paid_given_negative_payment_fulfills_it(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank sync',
        )
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333'
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=500,
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=-200,
        )
        promise1.refresh_from_db()
        assert promise1.status == STATUS_PAID

    def test_save_updates_status_to_underpaid_lesser_amount_is_received(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank sync',
        )
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333'
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=200,
        )
        promise1.refresh_from_db()
        assert promise1.status == STATUS_UNDERPAID

    def test_save_updates_status_to_overpaid_greater_amount_is_received(self):
        account = baker.make(
            'accounting.Account',
            name='Bank account',
            description='Bank sync',
        )
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333'
        )
        baker.make(
            'accounting.Statement',
            account=account,
            variable_symbol='333',
            amount=500,
        )
        promise1.refresh_from_db()
        assert promise1.status == STATUS_OVERPAID

    def test_creates_debt_given_none_are_present_and_amount_is_nonempty(self):
        today = datetime.date.today()
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333',
            start=today,
        )
        self.assert_equal_debts(promise1.debts.all(), [
            { 'amount': 300, 'promise': promise1, 'maturity': today, 'source': 2 },
        ])

    def test_creating_debt_from_default_source_recalculates_amount(self):
        today = datetime.date.today()
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333',
            start=today,
        )
        baker.make(
            'accounting.Debt',
            amount=600,
            promise=promise1,
        )
        promise1.refresh_from_db()
        assert promise1.amount == 900

    def test_creating_debt_from_manual_source_recalculates_amount(self):
        today = datetime.date.today()
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333',
            start=today,
        )
        baker.make(
            'accounting.Debt',
            amount=600,
            promise=promise1,
            source=DEBT_SOURCE_MANUAL,
        )
        promise1.refresh_from_db()
        assert promise1.amount == 900

    def test_creating_initial_debt_does_not_recalculate_amount(self):
        today = datetime.date.today()
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333',
            start=today,
        )
        baker.make(
            'accounting.Debt',
            amount=600,
            promise=promise1,
            source=DEBT_SOURCE_GENERATED_INITIAL,
        )
        promise1.refresh_from_db()
        assert promise1.amount == 300

    def test_creating_recurring_debt_does_not_recalculate_amount(self):
        today = datetime.date.today()
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333',
            start=today,
        )
        baker.make(
            'accounting.Debt',
            amount=600,
            promise=promise1,
            source=DEBT_SOURCE_GENERATED_RECURRING,
        )
        promise1.refresh_from_db()
        assert promise1.amount == 300

    @freeze_time('2020-03-01')
    def test_creates_debt_given_date_is_after(self):
        promise1 = baker.make(
            'accounting.Promise',
            variable_symbol='333',
            start=parse('2020-01-01').date(),
            repeat=RECURRENCE_MONTHLY,
            amount=300,
        )
        self.assert_equal_debts(promise1.debts.order_by('maturity').all(), [
            {
                'amount': 300,
                'promise': promise1,
                'maturity': parse('2020-01-01').date(),
                'source': 2,
            },
            {
                'amount': 300,
                'promise': promise1,
                'maturity': parse('2020-02-01').date(),
                'source': 3,
            },
            {
                'amount': 300,
                'promise': promise1,
                'maturity': parse('2020-03-01').date(),
                'source': 3,
            },
        ])

    @freeze_time('2020-02-27')
    def test_creates_debt_given_date_is_in_the_middle(self):
        promise1 = baker.make(
            'accounting.Promise',
            variable_symbol='333',
            start=parse('2020-01-01').date(),
            repeat=RECURRENCE_MONTHLY,
            amount=300,
        )
        self.assert_equal_debts(promise1.debts.order_by('maturity').all(), [
            {
                'amount': 300,
                'promise': promise1,
                'maturity': parse('2020-01-01').date(),
                'source': 2,
            },
            {
                'amount': 300,
                'promise': promise1,
                'maturity': parse('2020-02-01').date(),
                'source': 3,
            },
        ])

    @freeze_time('2020-03-01')
    def test_creates_debt_given_date_is_before(self):
        promise1 = baker.make(
            'accounting.Promise',
            variable_symbol='333',
            start=parse('2020-04-01').date(),
            repeat=RECURRENCE_MONTHLY,
            amount=300,
        )
        self.assert_equal_debts(promise1.debts.all(), [
            { 'amount':300, 'promise':promise1, 'maturity':parse('2020-04-01').date(), 'source': 2 }
        ])

class DebtTest(TestCase):
    def test_creating_recurring_debt_does_not_recalculate_amount(self):
        today = datetime.date.today()
        promise1 = baker.make(
            'accounting.Promise',
            amount=300,
            variable_symbol='333',
            start=today,
        )
        debt = baker.make(
            'accounting.Debt',
            amount=600,
            promise=promise1,
            source=DEBT_SOURCE_GENERATED_RECURRING,
        )
        assert str(debt) == '#2: 600 CZK'
