from django.db.models import BooleanField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .live_poll_type_field import LivePollTypeField


class LivePoll(TimeStampedModel):
    poll_type = LivePollTypeField()
    closed = BooleanField(default=False, verbose_name=_("Closed"),)

    class Meta:
        abstract = True

    def get_winning_option(self):
        winner = None
        loudest = 0
        votings = self.votings.all()
        for voting in votings:
            if voting.avg_volume is not None and (
                not winner or loudest < voting.avg_volume
            ):
                winner = voting
                loudest = voting.avg_volume
        return winner
