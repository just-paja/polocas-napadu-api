from django_extensions.db.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.db.models import ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _

from fields import NameMixin

from .statement_specs import StatementSenderSpecification


class CounterParty(NameMixin, TimeStampedModel):

    class Meta:
        verbose_name = _('Counterparty')
        verbose_name_plural = _('Counterparties')


class KnownAccount(StatementSenderSpecification, TimeStampedModel):

    class Meta:
        verbose_name = _('Known account')
        verbose_name_plural = _('Known accounts')
        unique_together = (
            ('sender_account_number', 'sender_bank'),
            ('sender_iban',),
        )

    owner = ForeignKey(
        'CounterParty',
        blank=False,
        null=False,
        on_delete=CASCADE,
        related_name='accounts',
    )

    def __str__(self):
        return '%s (%s)' % (self.owner.name, self.pk)

    def clean(self):
        if not (
            self.sender_account_number and
            self.sender_bank
        ) or (self.sender_iban and self.sender_bic):
            raise ValidationError(_('Fill in bank number and account number or IBAN and BIC'))

    def matches_statement(self, statement):
        matches = False
        if self.sender_account_number and self.sender_bank:
            matches = (
                self.sender_account_number == statement.sender_account_number and
                self.sender_bank == statement.sender_bank
            )
        if self.sender_iban and self.sender_bic:
            matches = matches and (
                self.sender_iban == statement.sender_iban and
                self.sender_bic == statement.sender_bic
            )
        return matches
