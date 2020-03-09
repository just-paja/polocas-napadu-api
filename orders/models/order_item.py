from django.db.models import ForeignKey, PositiveIntegerField, CASCADE, PROTECT
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from accounting.models.currency import AmountField, CurrencyField


class OrderItem(TimeStampedModel):
    order = ForeignKey(
        'Order',
        verbose_name=_('Order'),
        on_delete=CASCADE,
    )
    product = ForeignKey(
        'Orderable',
        verbose_name=_('Orderable'),
        on_delete=PROTECT,
    )
    price = AmountField(
        verbose_name=_('Price'),
        help_text=_('Item price at the time of order'),
    )
    currency = CurrencyField()
    quantity = PositiveIntegerField(
        verbose_name=_('Quantity'),
    )
