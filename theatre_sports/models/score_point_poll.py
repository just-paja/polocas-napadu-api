from django.db.models import Model, ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _

from voting.models import LivePollTypeField

class ScorePointPoll(Model):

    class Meta:
        verbose_name = _('Score Point Poll')
        verbose_name_plural = _('Score Point Polls')

    stage = ForeignKey(
        'MatchStage',
        on_delete=CASCADE,
        related_name='score_point_polls',
        verbose_name=_('Match Stage'),
    )
    winner = ForeignKey(
        'ScorePointPollVoting',
        on_delete=CASCADE,
        related_name='winning_polls',
        verbose_name=_('Winner'),
        null=True,
        blank=True,
    )
    poll_type = LivePollTypeField()

    def match(self):
        return self.stage.match.show.name

    def game(self):
        if self.stage.game:
            return self.stage.game.rules.name
        return None
