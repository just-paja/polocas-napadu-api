from django.db.models import ForeignKey, PROTECT
from django.utils.translation import ugettext_lazy as _

from events.models import Event


class Show(Event):
    class Meta:
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")

    show_type = ForeignKey(
        "ShowType",
        on_delete=PROTECT,
        related_name="shows",
        verbose_name=_("Show type"),
    )
