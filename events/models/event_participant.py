from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _


class EventParticipant(TimeStampedModel):
    class Meta:
        verbose_name = _("Event participant")
        verbose_name_plural = _("Event participants")

    event = ForeignKey(
        "events.Event",
        on_delete=CASCADE,
        related_name="eventParticipants",
        verbose_name=_("Event"),
    )
    profile = ForeignKey(
        "profiles.Profile",
        on_delete=CASCADE,
        related_name="eventsParticipated",
        verbose_name=_("Profile"),
    )
    role = ForeignKey(
        "events.ParticipantRole",
        on_delete=CASCADE,
        related_name="eventParticipants",
        verbose_name=_("Role"),
    )

    def __str__(self):
        return '%s (%s, %s)' % (
            self.profile.name,
            self.role.name,
            self.event.name
        )
