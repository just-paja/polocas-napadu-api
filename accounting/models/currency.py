from django.db.models import CharField, DecimalField
from django.utils.translation import gettext_lazy as _

CHOICES = [
    ('CZK', 'CZK'),
    ('EUR', 'EUR'),
    ('USD', 'USD'),
]


class AmountField(DecimalField):

    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = kwargs.get('decimal_places', 2)
        kwargs['default'] = kwargs.get('default', 0)
        kwargs['max_digits'] = kwargs.get('max_digits', 19)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Amount'))
        super().__init__(*args, **kwargs)


class CurrencyField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 3)
        kwargs['blank'] = kwargs.get('blank', False)
        kwargs['null'] = kwargs.get('null', False)
        kwargs['choices'] = kwargs.get('choices', CHOICES)
        kwargs['default'] = kwargs.get('default', 'CZK')
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Currency'))
        kwargs['help_text'] = kwargs.get(
            'help_text',
            _('ISO 4217 defined three letter currency abbreviation')
        )
        super().__init__(*args, **kwargs)
