from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from accounting.models.currency import AmountField, CurrencyField


class Orderable(TimeStampedModel):
    price = AmountField(
        verbose_name=_('Price'),
        help_text=_('Catalogue price of this item'),
    )
    currency = CurrencyField()

    @classmethod
    def max_quantity(cls):
        return 0
