from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from fields import DescriptionMixin, NameMixin, VisibilityMixin


class ShowType(
    NameMixin,
    DescriptionMixin,
    TimeStampedModel,
    VisibilityMixin
):
    class Meta:
        verbose_name = _('Show type')
        verbose_name_plural = _('Show types')
