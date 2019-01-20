from django.db.models import ForeignKey, PROTECT
from django.utils.translation import ugettext_lazy as _

from events.models import Event


class Show(Event):

    class Meta:
        verbose_name = _('Show')
        verbose_name_plural = _('Shows')

    show_type = ForeignKey('showType', on_delete=PROTECT)

    def get_inspiration_url(self):
        return 'https://tema.polocas-napadu.cz'
