import datetime
import pytest

from freezegun import freeze_time
from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker
from dateutil.parser import parse

from ..time_limited import TimeLimitedModel, intersects

class TimeLimitedTest(TestCase):
    @freeze_time('2020-03-01')
    def test_clean_allows_greater_end(self):
        today = datetime.date.today()
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            end=today + datetime.timedelta(days=1),
            name='test',
            start=today,
        )
        level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_equal_end(self):
        today = datetime.date.today()
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            end=today,
            name='test',
            start=today,
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_lower_end(self):
        today = datetime.date.today()
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            end=today - datetime.timedelta(days=1),
            name='test',
            start=today,
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_allows_unrelated_from_left(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-02-01',
            end='2020-02-29',
        )
        level.clean()

    @freeze_time('2020-03-01')
    def test_clean_allows_unrelated_from_right(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-04-01',
            end='2020-04-28',
        )
        level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_overlapping_from_left(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-02-01',
            end='2020-03-05',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_overlapping_from_right(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-25',
            end='2020-04-05',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_touching_from_left(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-02-01',
            end='2020-03-01',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_touching_from_right(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-31',
            end='2020-04-09',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_inner_touching_from_left(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-09',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_inner_touching_from_right(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-15',
            end='2020-03-31',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_inner(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-05',
            end='2020-03-09',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_unlimited_from_left(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-02-01',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-09',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_unlimited_from_inner(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-03',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-09',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_allows_unlimited_from_right(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-04-01',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
            end='2020-03-31',
        )
        level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_clashing_unlimited_from_right(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-04-01',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-05-01',
        )
        with pytest.raises(ValidationError):
            level.clean()

    @freeze_time('2020-03-01')
    def test_clean_blocks_clashing_unlimited_from_left(self):
        today = datetime.date.today()
        baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-04-01',
        )
        level = baker.make(
            'accounting.MembershipLevel',
            description='test',
            name='test',
            start='2020-03-01',
        )
        with pytest.raises(ValidationError):
            level.clean()


class IntersectionTest(TestCase):
    # ----------s------e-------------
    # ---s--e------------------------
    def test_returns_false_given_intervals_do_not_intersect_from_bottom_left(self):
        first = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=parse('2018-02-01'),
        )
        second = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=parse('2019-02-01'),
        )
        assert not intersects(first, second)

    # ---s--e------------------------
    # ----------s------e-------------
    def test_returns_false_given_intervals_do_not_intersect_from_top_left(self):
        second = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=parse('2018-02-01'),
        )
        first = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=parse('2019-02-01'),
        )
        assert not intersects(first, second)

    # ----------s------e-------------
    # ---s---------------------------
    def test_returns_true_given_earlier_has_no_end_from_bottom_left(self):
        first = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=None,
        )
        second = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=parse('2019-02-01'),
        )
        assert intersects(first, second)

    # ---s---------------------------
    # ----------s------e-------------
    def test_returns_true_given_earlier_has_no_end_from_top_left(self):
        second = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=None,
        )
        first = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=parse('2019-02-01'),
        )
        assert intersects(first, second)

    # ----------s--------------------
    # ---s----e----------------------
    def test_returns_false_given_later_has_no_end_and_dont_intersect_from_bottom_left(self):
        first = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=parse('2018-02-01'),
        )
        second = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=None,
        )
        assert not intersects(first, second)

    # ---s----e----------------------
    # ----------s--------------------
    def test_returns_false_given_later_has_no_end_and_dont_intersect_from_top_left(self):
        second = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=parse('2018-02-01'),
        )
        first = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=None,
        )
        assert not intersects(first, second)

    # ---s---------------------------
    # ----------s--------------------
    def test_returns_true_given_neither_interval_has_end(self):
        second = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=None,
        )
        first = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=None,
        )
        assert intersects(first, second)

    # ----------s------e-------------
    # ---s-------------e-------------
    def test_returns_false_given_have_equal_end_from_bottom_left(self):
        first = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=parse('2019-02-01'),
        )
        second = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=parse('2019-02-01'),
        )
        assert intersects(first, second)

    # ---s-------------e-------------
    # ----------s------e-------------
    def test_returns_false_given_have_equal_end_from_top_left(self):
        second = TimeLimitedModel(
            start=parse('2018-01-01'),
            end=parse('2019-02-01'),
        )
        first = TimeLimitedModel(
            start=parse('2019-01-01'),
            end=parse('2019-02-01'),
        )
        assert intersects(first, second)
