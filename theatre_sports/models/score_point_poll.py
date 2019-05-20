from django.db.models import (
    BooleanField,
    CASCADE,
    ForeignKey,
    Model,
    OneToOneField,
)
from django.utils.translation import ugettext_lazy as _

from voting.models import LivePollTypeField

class ScorePointPoll(Model):

    class Meta:
        verbose_name = _('Score Point Poll')
        verbose_name_plural = _('Score Point Polls')

    stage = OneToOneField(
        'MatchStage',
        on_delete=CASCADE,
        related_name='score_point_poll',
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
    closed = BooleanField(
        default=False,
        verbose_name=_('Closed'),
    )


    def match(self):
        return self.stage.match.show.name

    def game(self):
        if self.stage.game:
            return self.stage.game.rules.name
        return None

    def get_winning_option(self):
        winner = None
        loudest = 0
        votings = self.votings.all()
        for voting in votings:
            loudness = voting.get_average_loudness()
            if loudness is None and (not winner or loudest < loudness):
                winner = voting
                loudest = loudness
        return winner
