from django.utils.translation import ugettext_lazy as _

from accounting.models.currency import AmountField, CurrencyField
from fields import PublicResourceMixin


class PaymentMethod(PublicResourceMixin):

    class Meta:
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')

    price = AmountField()
    currency = CurrencyField()
