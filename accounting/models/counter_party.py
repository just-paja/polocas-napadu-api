from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin

from .statement_specs import StatementSenderSpecification


class CounterParty(NameMixin, TimeStampedModel):

    class Meta:
        verbose_name = _('CounterParty')
        verbose_name_plural = _('CounterParties')

    def count_known_accounts(self):
        return self.accounts.count()


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
