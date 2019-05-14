from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _

from voting.models import LivePollVoting

class ScorePointPollVoting(LivePollVoting):

    class Meta:
        verbose_name = _('Score point poll voting')
        verbose_name_plural = _('Score point poll votings')

    poll = ForeignKey(
        'ScorePointPoll',
        on_delete=CASCADE,
        related_name='votings',
        verbose_name=_('Score Point Poll'),
    )
    contestant_group = ForeignKey(
        'ContestantGroup',
        on_delete=CASCADE,
        related_name='score_point_poll_votings',
        verbose_name=_('Contestant Group'),
    )
