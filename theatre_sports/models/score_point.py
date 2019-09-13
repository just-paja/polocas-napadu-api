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

    def get_score_snapshot(self):
        return self.contestant_group.score_points.filter(
            created__lte=self.created,
        ).count()

    def get_contestant_group_name(self):
        return self.contestant_group.band.name

    def get_game_name(self):
        return self.game.rules.name

    def get_show_name(self):
        return self.game.show.name

    def get_show_date(self):
        return self.game.show.start


ScorePoint.get_contestant_group_name.short_description = _('Contestant')
ScorePoint.get_game_name.short_description = _('Game')
ScorePoint.get_score_snapshot.short_description = _('Score')
ScorePoint.get_show_date.short_description = _('Date')
ScorePoint.get_show_name.short_description = _('Match')
