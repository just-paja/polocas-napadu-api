from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from fields import NameMixin

class FoulType(NameMixin, TimeStampedModel):

    class Meta:
        verbose_name = _('FoulType')
        verbose_name_plural = _('Foul Types')

    description = TextField(
        verbose_name=_('Textual inspiration'),
    )
