from django.db.models import ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _

from voting.models import AlreadyClosed, LivePollVoting


class ScorePointPollVoting(LivePollVoting):
    class Meta:
        verbose_name = _("Score point poll voting")
        verbose_name_plural = _("Score point poll votings")

    poll = ForeignKey(
        "ScorePointPoll",
        on_delete=CASCADE,
        related_name="votings",
        verbose_name=_("Score Point Poll"),
    )
    contestant_group = ForeignKey(
        "ContestantGroup",
        on_delete=CASCADE,
        related_name="score_point_poll_votings",
        verbose_name=_("Contestant Group"),
    )

    def clean(self):
        if not self.pk and self.poll.closed:
            raise AlreadyClosed("Score Point Poll %s is already closed" % self.poll.pk)
