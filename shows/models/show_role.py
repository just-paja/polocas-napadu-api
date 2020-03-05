from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, WeightedMixin


class ShowRole(NameMixin, TimeStampedModel, WeightedMixin):
    class Meta:
        verbose_name = _("Show role")
        verbose_name_plural = _("Show roles")
