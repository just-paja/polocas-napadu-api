from django.db.models import CharField, ForeignKey, PositiveIntegerField, Sum, CASCADE

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from encrypted_fields.fields import EncryptedCharField

from fields import PublicResourceMixin

from .currency import CurrencyField

SCRAPE_SOURCE_MANUAL = 1
SCRAPE_SOURCE_CRON = 2

SCRAPE_SOURCE_CHOICES = (
    (SCRAPE_SOURCE_MANUAL, _('Manual')),
    (SCRAPE_SOURCE_CRON, _('Cron')),
)

SCRAPE_STATUS_REQUEST = 1
SCRAPE_STATUS_SUCCESS = 2
SCRAPE_STATUS_FAILURE = 3

SCRAPE_STATUS_CHOICES = (
    (SCRAPE_STATUS_REQUEST, _('Requested')),
    (SCRAPE_STATUS_SUCCESS, _('Succeeded')),
    (SCRAPE_STATUS_FAILURE, _('Failed')),
)


class AccountNumberField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Account number'))
        kwargs['help_text'] = kwargs.get(
            'help_text',
            _('Account number of person sending this payment')
        )
        super().__init__(*args, **kwargs)


class BankNumberField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 63
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Bank'))
        kwargs['help_text'] = kwargs.get(
            'help_text',
            _('Bank sending this payment')
        )
        super().__init__(*args, **kwargs)


class IBanField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('IBAN'))
        kwargs['help_text'] = kwargs.get(
            'help_text',
            _('International bank account number')
        )
        super().__init__(*args, **kwargs)


class BicField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('BIC'))
        kwargs['help_text'] = kwargs.get(
            'help_text',
            _('Business identification code, specified by SWIFT')
        )
        super().__init__(*args, **kwargs)


class Account(PublicResourceMixin):

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    currency = CurrencyField()
    account_number = AccountNumberField(blank=True, null=True)
    bank = BankNumberField(blank=True, null=True)
    iban = IBanField(blank=True, null=True)
    bic = BicField(blank=True, null=True)
    fio_readonly_key = EncryptedCharField(max_length=255, blank=True, null=True)

    def calculate_ballance(self):
        result = self.statements.aggregate(ballance=Sum('amount'))
        ballance = result['ballance']
        return ballance if ballance else 0

    def get_ballance(self):
        return '%.2f %s' % (self.calculate_ballance(), self.currency)

    get_ballance.short_description = _('Ballance')


class BankScrape(TimeStampedModel):
    account = ForeignKey(
        'Account',
        on_delete=CASCADE,
        related_name='scrapes',
        verbose_name=_('Account'),
    )
    days_back = PositiveIntegerField(
        null=True,
        blank=True,
    )
    source = PositiveIntegerField(
        default=SCRAPE_SOURCE_MANUAL,
        choices=SCRAPE_SOURCE_CHOICES,
    )
    status = PositiveIntegerField(
        default=SCRAPE_STATUS_REQUEST,
        choices=SCRAPE_STATUS_CHOICES,
    )
