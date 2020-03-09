from django.utils.translation import ugettext_lazy as _

from accounting.models.currency import AmountField, CurrencyField
from fields import PublicResourceMixin


class DeliveryMethod(PublicResourceMixin):

    class Meta:
        verbose_name = _('Delivery method')
        verbose_name_plural = _('Delivery methods')

    price = AmountField()
    currency = CurrencyField()
