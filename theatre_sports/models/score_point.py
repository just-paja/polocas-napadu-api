from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

class ScorePoint(TimeStampedModel):

    class Meta:
        verbose_name = _('ScorePoint')
        verbose_name_plural = _('ScorePoints')

    contestant_group = ForeignKey(
        'ContestantGroup',
        on_delete=CASCADE,
        related_name='score_points',
    )
    game = ForeignKey(
        'games.Game',
        on_delete=CASCADE,
        related_name='score_points',
    )
