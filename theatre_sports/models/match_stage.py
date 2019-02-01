from django.db.models import ForeignKey, PositiveIntegerField, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

STAGE_SHOW_SETUP = 1
STAGE_INTRO = 2
STAGE_GAME_SETUP = 3
STAGE_GAME = 4
STAGE_VOTING = 5
STAGE_GAME_RESULTS = 6
STAGE_PAUSE = 7
STAGE_FINALE = 8

STAGE_CHOICES = [
    (STAGE_SHOW_SETUP, _('stage-show-setup')),
    (STAGE_INTRO, _('stage-intro')),
    (STAGE_GAME_SETUP, _('stage-game-setup')),
    (STAGE_GAME, _('stage-game')),
    (STAGE_VOTING, _('stage-voting')),
    (STAGE_GAME_RESULTS, _('stage-game-results')),
    (STAGE_PAUSE, _('stage-pause')),
    (STAGE_FINALE, _('stage-finale')),
]

class MatchStage(TimeStampedModel):

    class Meta:
        verbose_name = _('Match Stage')
        verbose_name_plural = _('Match Stages')

    match = ForeignKey(
        'Match',
        on_delete=CASCADE,
        related_name='stages',
    )
    game = ForeignKey(
        'games.Game',
        blank=True,
        null=True,
        on_delete=PROTECT,
        related_name='stages',
    )
    type = PositiveIntegerField(
        choices=STAGE_CHOICES,
    )
