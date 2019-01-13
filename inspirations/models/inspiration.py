from django.db.models import BooleanField, CharField, ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _

from events.models import Event


class Inspiration(Event):

    class Meta:
        verbose_name = _('Inspiration')
        verbose_name_plural = _('Inspirations')

    show = ForeignKey('shows.Show', on_delete=CASCADE)
    text = CharField(
        max_length=255,
        verbose_name=_('Textual inspiration'),
        help_text=_('Enter words that will serve as an inspiration for this improvisation'),
    )
    discarded = BooleanField(default=False)
