# Level & Level fee
# -----------s-----------------es------------->
# Membership fee
#
# #1 --s-------------------------------------->
# #2 --s---------e---------------------------->
# #3 ------------s---------e------------------>
# #4 ------------s----------------------e----->
# #5 ---------------------------s-------e----->
# #6 ---------------------------s------------->
# #7 ------------------s---------------------->

from decimal import Decimal

import pytest

from freezegun import freeze_time
from django.core.exceptions import ValidationError
from django.test import TestCase
from dateutil.parser import parse
from model_bakery import baker


def promise_repr(promise):
    return {
        'initial_amount': promise.initial_amount,
        'currency': promise.currency,
        'end': promise.end,
        'level_fee': promise.level_fee,
        'repeat': promise.repeat,
        'start': promise.start,
    }

class MembershipTestBase(TestCase):
    maxDiff = 5000

    def setUp(self):
        self.level = baker.make(
            'accounting.MembershipLevel',
            name='Test Level',
            description='test',
        )
        self.level_fee_pre = baker.make(
            'accounting.MembershipLevelFee',
            currency='CZK',
            amount=Decimal('400.00'),
            level=self.level,
            start=parse('2017-01-01').date(),
            end=parse('2018-12-31').date(),
        )
        self.level_fee = baker.make(
            'accounting.MembershipLevelFee',
            currency='CZK',
            amount=Decimal('300.00'),
            level=self.level,
            start=parse('2019-01-01').date(),
        )
        self.user = baker.make(
            'auth.user',
            first_name='John',
            last_name='Boston',
        )

    def assert_equal_promises(self, actual, expected):
        return self.assertQuerysetEqual(actual, expected, promise_repr)


class MembershipTest(MembershipTestBase):
    @freeze_time('2020-03-01')
    def test_provides_user_name_in_string_representation(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2020-01-01').date(),
        )
        assert str(membership) == 'Členství: John Boston'

    @freeze_time('2020-03-01')
    def test_clean_rejects_overlapping_membership(self):
        baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2020-01-01').date(),
        )
        membership2 = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2022-01-01').date(),
        )
        with pytest.raises(ValidationError):
            membership2.clean()

    @freeze_time('2020-03-01')
    def test_membership_relates_to_same_member_memberships(self):
        membership1 = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2020-01-01').date(),
        )
        membership2 = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2022-01-01').date(),
        )
        def repr_pk(item):
            return item.pk
        self.assertQuerysetEqual(membership1.get_related_objects(), [membership2.pk], repr_pk)

    @freeze_time('2020-03-01')
    def test_membership_fee_relates_to_same_member_membership_fees(self):
        membership1 = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2020-01-01').date(),
        )
        membership2 = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2022-01-01').date(),
        )
        def repr_pk(item):
            return item.pk
        fee1 = membership1.fees.first()
        fee2 = membership2.fees.first()
        self.assertQuerysetEqual(fee1.get_related_objects(), [fee2.pk], repr_pk)


class MembershipCreateTest(MembershipTestBase):

    # -----------s-----------------es------------->
    # -----s-------------------------------------->
    @freeze_time('2020-03-01')
    def test_membership_has_free_period_two_paid_periods_and_no_end(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2016-06-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('400.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee_pre,
                'repeat': 'P1M',
                'start': parse('2017-01-01').date(),
                'end': parse('2018-12-31').date(),
            },
            {
                'initial_amount': Decimal('300.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee,
                'repeat': 'P1M',
                'start': parse('2019-01-01').date(),
                'end': None,
            },
        ), promise_repr)

    # -----------s-----------------es------------->
    # --s---------e------------------------------->
    @freeze_time('2020-03-01')
    def test_membership_has_free_period_and_one_closed_paid_period(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2016-06-01').date(),
            end=parse('2017-02-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('400.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee_pre,
                'repeat': 'P1M',
                'start': parse('2017-01-01').date(),
                'end': parse('2017-02-01').date(),
            },
        ), promise_repr)

    # -----------s-----------------es------------->
    # ------------s---------e--------------------->
    @freeze_time('2020-03-01')
    def test_membership_has_a_closed_paid_period(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2017-02-01').date(),
            end=parse('2018-01-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('400.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee_pre,
                'repeat': 'P1M',
                'start': parse('2017-02-01').date(),
                'end': parse('2018-01-01').date(),
            },
        ), promise_repr)

    # -----------s-----------------es------------->
    # ---------------s----------------------e----->
    @freeze_time('2020-03-01')
    def test_membership_has_two_closed_paid_periods(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2017-06-01').date(),
            end=parse('2020-06-01').date()
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('400.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee_pre,
                'repeat': 'P1M',
                'start': parse('2017-06-01').date(),
                'end': parse('2018-12-31').date(),
            },
            {
                'initial_amount': Decimal('300.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee,
                'repeat': 'P1M',
                'start': parse('2019-01-01').date(),
                'end': parse('2020-06-01').date(),
            },
        ), promise_repr)

    # -----------s-----------------es------------->
    # ------------------------------s-------e----->
    @freeze_time('2020-03-01')
    def test_membership_has_a_closed_paid_period_after_fee_change(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2019-01-01').date(),
            end=parse('2019-06-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('300.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee,
                'repeat': 'P1M',
                'start': parse('2019-01-01').date(),
                'end': parse('2019-06-01').date(),
            },
        ), promise_repr)

    # -----------s-----------------es------------->
    # ------------------------------s------------->
    @freeze_time('2020-03-01')
    def test_membership_has_an_open_paid_period_after_fee_change(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2019-01-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('300.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee,
                'repeat': 'P1M',
                'start': parse('2019-01-01').date(),
                'end': None,
            },
        ), promise_repr)

    # -----------s-----------------es------------->
    # ---------------------s---------------------->
    @freeze_time('2020-03-01')
    def test_membership_has_a_closed_paid_period_and_open_paid_period_after_fee_change(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2018-06-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('400.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee_pre,
                'repeat': 'P1M',
                'start': parse('2018-06-01').date(),
                'end': parse('2018-12-31').date(),
            },
            {
                'initial_amount': Decimal('300.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee,
                'repeat': 'P1M',
                'start': parse('2019-01-01').date(),
                'end': None,
            },
        ), promise_repr)

    # -----------s----e------------es------------->
    # ---------------------s---------------------->
    @freeze_time('2020-03-01')
    def test_membership_has_a_free_period_and_open_period_given_it_starts_in_hole(self):
        baker.make(
            'accounting.MembershipLevelFee',
            currency='CZK',
            amount=Decimal('300.00'),
            level=self.level,
            start=parse('2012-01-01').date(),
            end=parse('2013-01-01').date(),
        )
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2018-06-01').date(),
        )
        self.assertQuerysetEqual(membership.fees.order_by('start').all(), (
            {
                'initial_amount': Decimal('400.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee_pre,
                'repeat': 'P1M',
                'start': parse('2018-06-01').date(),
                'end': parse('2018-12-31').date(),
            },
            {
                'initial_amount': Decimal('300.00'),
                'currency': 'CZK',
                'level_fee': self.level_fee,
                'repeat': 'P1M',
                'start': parse('2019-01-01').date(),
                'end': None,
            },
        ), promise_repr)


class MembershipUpdateTest(MembershipTestBase):

    @freeze_time('2020-03-01')
    def test_remembers_manual_debt_changes(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2018-06-01').date(),
        )
        debt = membership.fees.first().debts.first()
        debt.amount = 0
        debt.save()
        membership.refresh_from_db()
        membership.save()
        assert membership.fees.first().debts.first().amount == Decimal('0.00')

    @freeze_time('2020-03-01')
    def test_deletes_void_promises(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2018-06-01').date(),
        )
        membership.refresh_from_db()
        membership.start = parse('2019-01-01').date()
        membership.save()
        membership.refresh_from_db()
        assert membership.fees.first().level_fee == self.level_fee

    @freeze_time('2020-03-01')
    def test_updates_fees_dates(self):
        membership = baker.make(
            'accounting.Membership',
            level=self.level,
            user=self.user,
            start=parse('2019-01-01').date(),
        )
        membership.start = parse('2019-06-01').date()
        membership.save()
        assert membership.fees.first().start == parse('2019-06-1').date()


class MembershipLevelFeeModelTest(MembershipTestBase):
    def test_repr(self):
        assert str(self.level_fee) == '300.00 CZK (Test Level)'
