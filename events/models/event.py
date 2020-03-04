from django_extensions.db.fields import AutoSlugField
from django.db.models import (
    BooleanField,
    DateTimeField,
    EmailField,
    ForeignKey,
    URLField,
    PROTECT,
)
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin, VisibilityManager


class EventManager(VisibilityManager):
    def get_recent(self):
        return self.get_visible().order("-start")


class Event(PublicResourceMixin):
    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
    start = DateTimeField()
    end = DateTimeField(blank=True, null=True)
    all_day = BooleanField(default=False)
    location = ForeignKey("locations.Location", on_delete=PROTECT)
    objects = EventManager()
    email_reservations = EmailField(
        blank=True,
        null=True,
        verbose_name=_('Reservation e-mail'),
    )
    link_facebook = URLField(
        blank=True,
        null=True,
        verbose_name=_('Event on Facebook'),
    )
    link_reservations = URLField(
        blank=True,
        null=True,
        verbose_name=_('Reservation link'),
    )
    link_tickets = URLField(
        blank=True,
        null=True,
        verbose_name=_('Link to buy tickets'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "%s, %s" % (self.name, date_format(self.start, "DATE_FORMAT"),)
