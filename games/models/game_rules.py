from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from fields import DescriptionMixin, NameMixin, VisibilityMixin


class GameRules(
    DescriptionMixin,
    NameMixin,
    VisibilityMixin,
    TimeStampedModel
):
    class Meta:
        verbose_name = _('Game Rule')
        verbose_name_plural = _('Game Rules')
