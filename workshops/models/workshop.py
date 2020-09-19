from django.utils.translation import ugettext_lazy as _
from django.db.models import PositiveIntegerField

from events.models import Event


class Workshop(Event):
    class Meta:
        verbose_name = _("Workshops")
        verbose_name_plural = _("Workshops")

    capacity = PositiveIntegerField(
        default=12,
        verbose_name=_('Capacity'),
    )
