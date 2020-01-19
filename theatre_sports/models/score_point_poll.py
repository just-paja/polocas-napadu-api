from django.db.models import CASCADE, ForeignKey, OneToOneField
from django.utils.translation import ugettext_lazy as _

from voting.models import LivePoll


class ScorePointPoll(LivePoll):
    class Meta:
        verbose_name = _("Score Point Poll")
        verbose_name_plural = _("Score Point Polls")

    stage = OneToOneField(
        "MatchStage",
        on_delete=CASCADE,
        related_name="score_point_poll",
        verbose_name=_("Match Stage"),
    )
    winner = ForeignKey(
        "ScorePointPollVoting",
        on_delete=CASCADE,
        related_name="winning_polls",
        verbose_name=_("Winner"),
        null=True,
        blank=True,
    )

    def match(self):
        return self.stage.match.show.name

    def game(self):
        if self.stage.game:
            return self.stage.game.rules.name
        return None
