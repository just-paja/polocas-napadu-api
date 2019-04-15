from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from fields import DescriptionMixin, NameMixin

class FoulType(
    NameMixin,
    DescriptionMixin,
    TimeStampedModel
):
    class Meta:
        verbose_name = _('FoulType')
        verbose_name_plural = _('Foul Types')
