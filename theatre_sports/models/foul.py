from django.db.models import TextField, ForeignKey, CASCADE
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
        related_name='fouls',
    )
    comment = TextField(
        max_length=255,
        verbose_name=_('Textual inspiration'),
        help_text=_('Enter words that will serve as an inspiration for this improvisation'),
    )
