from django_extensions.db.fields import AutoSlugField
from django.db.models import (
    BooleanField,
    DateTimeField,
    EmailField,
    ForeignKey,
    ManyToManyField,
    URLField,
    PROTECT,
)
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from fields import DescriptionField, PublicResourceMixin, VisibilityManager


class EventManager(VisibilityManager):
    def get_recent(self):
        return self.get_visible().order("-start")


class Event(PublicResourceMixin):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
    description = DescriptionField(blank=True, null=True)
    start = DateTimeField(verbose_name=_("Start"))
    end = DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("End"),
    )
    all_day = BooleanField(
        default=False,
        verbose_name=_("All day")
    )
    canceled = BooleanField(
        default=False,
        verbose_name=_('Canceled'),
        help_text=_('Event has been canceled'),
    )
    location = ForeignKey(
        "locations.Location",
        on_delete=PROTECT,
        verbose_name=_("Location"),
    )
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
    sponsors = ManyToManyField("profiles.Sponsor", blank=True)

    def __str__(self):
        return "%s, %s" % (self.name, date_format(self.start, "DATE_FORMAT"),)
