from django.db.models import ForeignKey, ManyToManyField, PositiveIntegerField, CASCADE, PROTECT
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
        verbose_name=_('Match'),
    )
    game = ForeignKey(
        'games.Game',
        blank=True,
        null=True,
        on_delete=PROTECT,
        related_name='stages',
        verbose_name=_('Game'),
    )
    type = PositiveIntegerField(
        choices=STAGE_CHOICES,
        verbose_name=_('Stage Type'),
    )
    inspirations = ManyToManyField(
        'inspirations.Inspiration',
        blank=True,
        related_name='stages',
        verbose_name=_('Inspirations'),
    )

    def __str__(self):
        return '%s, %s' % (
            self.get_type_display(),
            self.match.show,
        )

    def pass_game_to_next_stage(self):
        return self.type in [
            STAGE_GAME_SETUP,
            STAGE_GAME,
            STAGE_VOTING,
        ]

    def get_game_name(self):
        if self.game:
            return self.game.rules.name
        return None

    def show(self):
        return self.match.show

    def get_duration(self):
        next_stage = self.match.stages.filter(
            created__gt=self.created
        ).order_by('created').first()
        if next_stage:
            return next_stage.created - self.created
        return None

MatchStage.get_game_name.short_description = _('Game')
MatchStage.get_duration.short_description = _('Duration')
