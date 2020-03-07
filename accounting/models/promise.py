import datetime

from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    ForeignKey,
    PROTECT,
    Sum,
    PositiveIntegerField
)

from dateutil.relativedelta import relativedelta
from fields import DescriptionField, NameField

from .currency import AmountField, CurrencyField
from .statement_specs import StatementSpecification
from .time_limited import TimeLimitedModel, TimeLimitedManager

STATUS_EXPECTED = 1
STATUS_PAID = 2
STATUS_UNDERPAID = 3
STATUS_OVERPAID = 4

STATUS_CHOICES = (
    (STATUS_EXPECTED, _('Expected')),
    (STATUS_PAID, _('Paid')),
    (STATUS_UNDERPAID, _('Underpaid')),
    (STATUS_OVERPAID, _('Overpaid')),
)

RECURRENCE_NONE = None
RECURRENCE_MONTHLY = 'P1M'
RECURRENCE_YEARLY = 'P1Y'

RECURRENCE_CHOICES = (
    (RECURRENCE_NONE, _('Never')),
    (RECURRENCE_MONTHLY, _('Monthly')),
    (RECURRENCE_YEARLY, _('Yearly')),
)


class PromiseManager(TimeLimitedManager):
    def filter_by_transaction(self, variable_symbol, specific_symbol):
        query = self.filter(variable_symbol=variable_symbol)
        if specific_symbol:
            query = query.filter(specific_symbol=specific_symbol)
        return query


class Promise(StatementSpecification, TimeLimitedModel):

    class Meta:
        verbose_name = _('Promise')
        verbose_name_plural = _('Promises')
        unique_together = (('variable_symbol',),)

    objects = PromiseManager()
    initial_amount = AmountField(
        verbose_name=_('Initial amount'),
    )
    purpose = ForeignKey(
        'accounting.Purpose',
        blank=False,
        null=True,
        on_delete=PROTECT,
        related_name='promises',
    )
    status = PositiveIntegerField(
        default=STATUS_EXPECTED,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
    )
    name = NameField(
        blank=True,
        max_length=127,
        null=True,
    )
    repeat = CharField(
        blank=True,
        choices=RECURRENCE_CHOICES,
        max_length=31,
        null=True,
        verbose_name=_('Repeat'),
    )

    def __str__(self):
        return self.name if self.name else 'Promise#%s' % self.id

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        if not self.pk:
            self.initial_amount = self.amount
            super().save(*args, **kwargs)
        self.create_debts()
        self.amount = self.calculate_amount()
        self.status = self.calculate_status()
        super().save(*args, **kwargs)

    def get_volume_price_tag(self):
        return '%s' % (self.sum_statements())

    def calculate_status(self):
        received = self.sum_statements()
        if received == 0:
            return STATUS_EXPECTED
        if received > self.amount:
            return STATUS_OVERPAID
        if received < self.amount:
            return STATUS_UNDERPAID
        return STATUS_PAID

    def create_debts(self):
        self.create_initial_debt()
        self.create_recurrent_debts()

    def create_recurrent_debts(self):
        delta = self.get_recurrence_delta()
        if delta:
            today = datetime.date.today()
            date = self.start + delta
            end = today if not self.end or self.end > today else self.end
            while date <= end:
                self.ensure_recurrent_debt(date)
                date += delta

    def ensure_recurrent_debt(self, date):
        delta = self.get_recurrence_delta()
        if delta:
            debt = self.debts.filter(
                maturity=date,
                source=DEBT_SOURCE_GENERATED_RECURRING,
            ).first()
            if debt:
                return debt
            debt = Debt(
                amount=self.initial_amount,
                currency=self.currency,
                maturity=date,
                promise=self,
                source=DEBT_SOURCE_GENERATED_RECURRING,
            )
            debt.save()
            return debt
        return None

    def create_initial_debt(self):
        if self.debts.count() == 0 and self.amount != 0:
            debt = Debt(
                amount=self.amount,
                currency=self.currency,
                maturity=self.start,
                promise=self,
                source=DEBT_SOURCE_GENERATED_INITIAL,
            )
            debt.save()

    def calculate_amount(self):
        result = self.debts.aggregate(amount=Sum('amount'))
        return result.get('amount', 0) or 0

    def get_recurrence_delta(self):
        if self.repeat == RECURRENCE_MONTHLY:
            return relativedelta(months=1)
        if self.repeat == RECURRENCE_YEARLY:
            return relativedelta(years=1)
        return None

    def sum_statements(self):
        result = self.statements.aggregate(ballance=Sum('amount'))
        ballance = result['ballance']
        return ballance if ballance else 0

    def get_amount_diff(self):
        return self.sum_statements() - self.calculate_amount()

    get_volume_price_tag.short_description = _('Received')


DEBT_SOURCE_MANUAL = 1
DEBT_SOURCE_GENERATED_INITIAL = 2
DEBT_SOURCE_GENERATED_RECURRING = 3

DEBT_SOURCE_CHOICES = (
    (DEBT_SOURCE_MANUAL, _('Manually created')),
    (DEBT_SOURCE_GENERATED_INITIAL, _('Initial debt')),
    (DEBT_SOURCE_GENERATED_RECURRING, _('Recurring generated')),
)


class Debt(TimeStampedModel):

    class Meta:
        verbose_name = _('Debt')
        verbose_name_plural = _('Debts')

    promise = ForeignKey('Promise', on_delete=CASCADE, related_name='debts')
    amount = AmountField()
    currency = CurrencyField()
    source = PositiveIntegerField(
        default=DEBT_SOURCE_MANUAL,
        choices=DEBT_SOURCE_CHOICES,
    )
    description = DescriptionField(blank=True, null=True)
    maturity = DateField(
        verbose_name=_('Maturity'),
    )

    def __str__(self):
        return '#%s: %s %s' % (self.pk, self.amount, self.currency)

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        super().save()
        if self.source == DEBT_SOURCE_MANUAL:
            self.promise.save(*args, **kwargs)
