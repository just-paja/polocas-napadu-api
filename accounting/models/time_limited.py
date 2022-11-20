import datetime

from django.core.exceptions import ValidationError
from django.db.models import DateField, Manager, Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class TimeLimitedModel(TimeStampedModel):

    class Meta:
        abstract = True

    start = DateField(
        verbose_name=_('Start'),
        default=now,
    )
    end = DateField(
        blank=True,
        null=True,
        verbose_name=_('End')
    )

    def is_active(self):
        today = datetime.date.today()
        return self.start <= today and (not self.end or self.end > today)

    is_active.boolean = True
    is_active.short_description = _('Active')


class TimeFilteredModel(TimeLimitedModel):

    class Meta:
        abstract = True

    def get_related_objects(self):
        return self.__class__.objects.exclude(pk=self.pk)

    def clean(self):
        if self.end:
            if self.start >= self.end:
                raise ValidationError({
                    'end': _('End must be blank of greater than start'),
                })
        query = Q(start__lte=self.start, end__isnull=True)
        if self.end:
            query = query | Q(end__isnull=False, start__lte=self.end, end__gte=self.end)
            query = query | Q(end__isnull=False, end__gte=self.start, end__lte=self.end)
            query = query | Q(end__isnull=True, start__lte=self.end)
        else:
            query = query | Q(end__isnull=True)
            query = query | Q(end__isnull=False, end__gte=self.start)
        clashes = self.get_related_objects().filter(query)
        if clashes.count() > 0:
            raise ValidationError(_('Selected interval clashes with %s' % (clashes[0])))


class TimeLimitedManager(Manager):

    def get_active(self, date=None):
        filter_date = date if date else datetime.date.today()
        return self.filter(Q(end__isnull=True) | Q(end__gte=filter_date), start__lte=filter_date)

    def get_next(self, date=None):
        return self.filter(start__gt=date)


def sooner(date1, date2):
    if date1 and date2:
        return date1 if date1 < date2 else date2
    return date1 or date2


def later(date1, date2):
    if date1 and date2:
        return date1 if date1 > date2 else date2
    return date1 or date2


def intersects(interval1, interval2):
    if not interval1.end and not interval2.end:
        return True
    if interval1.start > interval2.start:
        earlier_object = interval2
        later_object = interval1
    else:
        earlier_object = interval1
        later_object = interval2
    if not earlier_object.end:
        return True
    if later_object.start <= earlier_object.end:
        return True
    return False
