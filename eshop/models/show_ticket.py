from django.db.models import DateTimeField, ForeignKey, PROTECT
from django.utils.translation import ugettext_lazy as _

from orders.models import Orderable


class ShowTicket(Orderable):
    show_ticket_price = ForeignKey(
        'shows.ShowTicketPrice',
        verbose_name=_('Show ticket price'),
        on_delete=PROTECT,
    )
    used_on = DateTimeField(
        blank=True,
        help_text=_('Exact time the ticket was used'),
        null=True,
        verbose_name=_('Used on'),
    )

    @classmethod
    def max_quantity(cls):
        # There can be only one ticket of a kind
        return 1
