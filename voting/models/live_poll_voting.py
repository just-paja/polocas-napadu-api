from django.db.models import Avg, BooleanField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .live_poll_type_field import LivePollTypeField


class LivePollVoting(TimeStampedModel):
    vote_type = LivePollTypeField()
    closed = BooleanField(
        default=False,
        verbose_name=_('Closed'),
    )

    class Meta:
        verbose_name = _('Live Poll Voting')
        verbose_name_plural = _('Live Poll Votings')

    def get_average_loudness(self):
        values = self.volume_scrapes.aggregate(Avg('volume')).values()
        return max(values)
