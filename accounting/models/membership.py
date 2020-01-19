from django.db.models import ForeignKey, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, DescriptionMixin

from .currency import AmountField, CurrencyField
from .promise import Promise, RECURRENCE_MONTHLY
from .time_limited import TimeLimitedManager, TimeFilteredModel, intersects, later, sooner

MEMBERSHIP_NAME_IDENTIFIER = 'Členství'


def format_membership_name(user):
    return '%s: %s' % (
        MEMBERSHIP_NAME_IDENTIFIER,
        user.get_full_name() or user.username
    )


class Membership(TimeFilteredModel):

    class Meta:
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')

    objects = TimeLimitedManager()
    level = ForeignKey('MembershipLevel', on_delete=PROTECT, related_name='memberships')
    user = ForeignKey('auth.User', on_delete=PROTECT, related_name='memberships')

    def __str__(self):
        return format_membership_name(self.user)

    def get_related_objects(self):
        return super().get_related_objects().filter(user=self.user)

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        super().save(*args, **kwargs)
        self.update_fees()

    def update_fees(self):
        level_fees = MembershipLevelFee.objects.filter(level=self.level).order_by('start').all()
        for level_fee in level_fees:
            if intersects(level_fee, self):
                fee = self.fees.filter(level_fee=level_fee).first() or MembershipFee()
                fee.amount = level_fee.amount
                fee.currency = level_fee.currency
                fee.end = sooner(self.end, level_fee.end)
                fee.level_fee = level_fee
                fee.membership = self
                fee.start = later(self.start, level_fee.start)
                fee.save()
            else:
                fees = self.fees.filter(level_fee=level_fee)
                for fee in fees:
                    fee.delete()


class MembershipLevel(NameMixin, DescriptionMixin, TimeFilteredModel):

    class Meta:
        verbose_name = _('Membership level')
        verbose_name_plural = _('Membership levels')

    objects = TimeLimitedManager()

    def __str__(self):
        return self.name


class MembershipLevelFee(TimeFilteredModel):

    class Meta:
        verbose_name = _('Membership level')
        verbose_name_plural = _('Membership levels')

    objects = TimeLimitedManager()
    level = ForeignKey(
        'MembershipLevel',
        on_delete=CASCADE
    )
    amount = AmountField()
    currency = CurrencyField()

    def __str__(self):
        return '%s %s (%s)' % (self.amount, self.currency, self.level.name)


class MembershipFee(Promise):

    class Meta:
        verbose_name = _('Membership fee')
        verbose_name_plural = _('Membership fees')

    membership = ForeignKey(
        'Membership',
        on_delete=CASCADE,
        related_name='fees',
    )
    level_fee = ForeignKey(
        'MembershipLevelFee',
        on_delete=PROTECT,
        related_name='fees',
    )

    def save(self, *args, **kwargs):
        self.repeat = RECURRENCE_MONTHLY
        self.name = format_membership_name(self.membership.user)
        super().save(*args, **kwargs)

    def get_related_objects(self):
        return super().get_related_objects().filter(membership__user=self.membership.user)
