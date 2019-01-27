from django_extensions.db.models import TimeStampedModel
from django.db.models import (
    DateTimeField,
    PositiveIntegerField,
    ForeignKey,
    ManyToManyField,
    CASCADE,
    PROTECT,
)
from django.utils.translation import ugettext_lazy as _


class Game(TimeStampedModel):

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

    show = ForeignKey(
        'shows.Show',
        on_delete=CASCADE,
        related_name='games',
    )
    rules = ForeignKey(
        'GameRules',
        on_delete=PROTECT,
        related_name='games',
    )
    inspirations = ManyToManyField(
        'inspirations.Inspiration',
        related_name='inspiration_games',
    )

    time_limit = PositiveIntegerField(blank=True, null=True)
    start = DateTimeField(blank=True, null=True)
    end = DateTimeField(blank=True, null=True)
