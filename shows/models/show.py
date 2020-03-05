from django.db.models import ForeignKey, PROTECT
from django.utils.translation import ugettext_lazy as _

from accounting.models import AmountField, CurrencyField
from events.models import Event
from fields import DescriptionField


class Show(Event):
    class Meta:
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")

    description = DescriptionField(blank=True, null=True)
    show_type = ForeignKey(
        "showType",
        on_delete=PROTECT,
        related_name="shows",
        verbose_name=_("Show type"),
    )
