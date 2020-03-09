from django.db.models import Model, ForeignKey, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _

from accounting.models import AmountField, CurrencyField


class ShowTicketPrice(Model):
    class Meta:
        verbose_name = _('Show ticket price')
        verbose_name_plural = _('Show ticket prices')

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
    amount = AmountField()
    currency = CurrencyField()


    def __str__(self):
        return '%s %s %s (%s)' % (
            self.show.name,
            self.amount,
            self.currency,
            self.price_level.name,
        )
