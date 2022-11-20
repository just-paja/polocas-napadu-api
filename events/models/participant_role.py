from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

from fields import NameMixin, WeightedMixin


class ParticipantRole(NameMixin, TimeStampedModel, WeightedMixin):
    class Meta:
        verbose_name = _("Participant role")
        verbose_name_plural = _("Participant roles")
