from django.db.models import Model, PositiveIntegerField
from django.utils.translation import ugettext_lazy as _

from .account import AccountNumberField, BankNumberField, IBanField, BicField
from .currency import AmountField, CurrencyField


class StatementSpecification(Model):

    class Meta:
        abstract = True

    amount = AmountField()
    currency = CurrencyField()
    variable_symbol = PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('variableSymbol'),
        help_text=_('Optional payment identifier'),
    )
    constant_symbol = PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('constantSymbol'),
        help_text=_('Purpose code of the payment specified by Czech banking system.'),
    )
    specific_symbol = PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Specific symbol'),
        help_text=_('This number focuses variable symbol.'),
    )


class StatementSenderSpecification(Model):

    class Meta:
        abstract = True

    sender_account_number = AccountNumberField(blank=True, null=True)
    sender_bank = BankNumberField(blank=True, null=True)
    sender_iban = IBanField(blank=True, null=True)
    sender_bic = BicField(blank=True, null=True)
