from django.db.models import BooleanField, ForeignKey, PositiveIntegerField, PROTECT
from django.utils.translation import ugettext_lazy as _

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
    sell_tickets = BooleanField(
        default=False,
        verbose_name=_('Sell tickets'),
        help_text=_('Ticketing system will be enabled for this show'),
    )
    capacity = PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Capacity'),
        help_text=_('Maximum amount of tickets to be sold'),
    )
