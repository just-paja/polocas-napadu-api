from django.db.models import Avg, BooleanField, FloatField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .live_poll_type_field import LivePollTypeField


class LivePollVoting(TimeStampedModel):
    vote_type = LivePollTypeField()
    closed = BooleanField(default=False, verbose_name=_("Closed"),)
    avg_volume = FloatField(
        blank=True,
        help_text=_("avgVolumeHelpText"),
        null=True,
        verbose_name=_("Average volume"),
    )

    class Meta:
        verbose_name = _("Live Poll Voting")
        verbose_name_plural = _("Live Poll Votings")

    def get_average_loudness(self):
        values = self.volume_scrapes.aggregate(Avg("volume")).values()
        return max(values)

    def close(self):
        self.avg_volume = self.get_average_loudness()
        self.closed = True
        self.save()
