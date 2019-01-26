from django.db.models import Model, ForeignKey, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _


class GameInspiration(Model):

    class Meta:
        verbose_name = _('Game Inspiration')
        verbose_name_plural = _('Game Inspirations')

    game = ForeignKey(
        'Game',
        on_delete=CASCADE,
        related_name='game_inspirations',
    )
    inspiration = ForeignKey(
        'inspirations.Inspiration',
        on_delete=PROTECT,
        related_name='inspiration_games',
    )
