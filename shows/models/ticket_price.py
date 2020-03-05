from django.db.models import Model, ForeignKey, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _

from accounting.models import AmountField, CurrencyField


class TicketPrice(Model):
    show = ForeignKey(
        'Show',
        on_delete=CASCADE,
        related_name='ticket_prices',
        verbose_name=_('Show'),
    )
    price_level = ForeignKey(
        'accounting.PriceLevel',
        on_delete=PROTECT,
        related_name='ticket_prices',
        verbose_name=_('Price level'),
    )
    price = AmountField()
    currency = CurrencyField()
