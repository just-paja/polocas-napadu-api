from django.db.models import Model, ForeignKey, CASCADE, PROTECT
from django.utils.translation import gettext_lazy as _

from accounting.models import AmountField, CurrencyField


class EventTicketPrice(Model):
    event = ForeignKey(
        'events.Event',
        on_delete=CASCADE,
        related_name='ticket_prices',
        verbose_name=_('Event'),
    )
    price_level = ForeignKey(
        'accounting.PriceLevel',
        on_delete=PROTECT,
        related_name='event_ticket_prices',
        verbose_name=_('Price level'),
    )
    amount = AmountField()
    currency = CurrencyField()
