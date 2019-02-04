from django.db.models import TextField, ForeignKey, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

class Foul(TimeStampedModel):

    class Meta:
        verbose_name = _('Foul')
        verbose_name_plural = _('Fouls')

    match = ForeignKey(
        'Match',
        on_delete=CASCADE,
        related_name='fouls',
    )
    contestant_group = ForeignKey(
        'ContestantGroup',
        on_delete=CASCADE,
        related_name='fouls',
    )
    game = ForeignKey(
        'games.Game',
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='fouls',
    )
    foul_type = ForeignKey(
        'FoulType',
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name='fouls',
    )
    comment = TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Describe what was the foul play'),
    )
