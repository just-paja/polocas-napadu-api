from django.db.models import BooleanField, OneToOneField, CASCADE
from django.utils.translation import ugettext_lazy as _

from events.models import Event


class Match(Event):

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    show = OneToOneField(
        'shows.Show',
        on_delete=CASCADE,
        related_name='match',
    )
    closed = BooleanField(
        default=False,
    )
