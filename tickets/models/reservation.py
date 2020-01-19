from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models import (
    CASCADE,
    BooleanField,
    EmailField,
    ForeignKey,
    CharField,
    PositiveIntegerField,
)

STATUS_ORDERED = 1
STATUS_CONFIRMED = 2
STATUS_CANCELED = 3

STATUS_CHOICES = [
    (STATUS_ORDERED, _("Ordered")),
    (STATUS_CONFIRMED, _("Confirmed")),
    (STATUS_CANCELED, _("Canceled")),
]

SEAT_LOCATION_WHATEVER = 1
SEAT_LOCATION_FIRST_ROW = 2
SEAT_LOCATION_MIDDLE = 3
SEAT_LOCATION_FAR_END = 4

SEAT_LOCATION_CHOICES = [
    (SEAT_LOCATION_WHATEVER, _("Whatever")),
    (SEAT_LOCATION_FIRST_ROW, _("First row")),
    (SEAT_LOCATION_MIDDLE, _("Middle")),
    (SEAT_LOCATION_FAR_END, _("Far end")),
]


class Reservation(TimeStampedModel):
    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    show = ForeignKey("shows.Show", on_delete=CASCADE,)
    customer_name = CharField(max_length=63, verbose_name=_("Customer name"),)
    customer_email = EmailField(verbose_name=_("Customer email"),)
    seat_count = PositiveIntegerField(default=1, verbose_name=_("Number of seats"),)
    seat_location = PositiveIntegerField(
        choices=SEAT_LOCATION_CHOICES, verbose_name=_("Seat location"),
    )
    status = PositiveIntegerField(choices=STATUS_CHOICES, verbose_name=_("Status"),)
    newsletter = BooleanField(default=False, verbose_name=_("Newsletter"),)
