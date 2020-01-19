import datetime

from django.utils import timezone
from fiobank import FioBank

from .models import (
    BankScrape,
    SCRAPE_SOURCE_MANUAL,
    SCRAPE_STATUS_FAILURE,
    SCRAPE_STATUS_REQUEST,
    SCRAPE_STATUS_SUCCESS,
    Statement,
)


def sync_fio(account, days_back, source=SCRAPE_SOURCE_MANUAL):
    scrape = BankScrape(
        account=account,
        days_back=days_back,
        source=source,
        status=SCRAPE_STATUS_REQUEST,
    )
    scrape.save()
    try:
        client = FioBank(token=account.fio_readonly_key)
        gen = client.period(
            datetime.datetime.now() - datetime.timedelta(days=days_back),
            datetime.datetime.now(),
        )
        for line in gen:
            Statement.objects.get_or_create(
                ident=line['transaction_id'],
                account=account,
                defaults={
                    'amount': line.get('amount', None),
                    'constant_symbol': line.get('constant_symbol', None),
                    'currency': line.get('currency', None),
                    'message': line.get('recipient_message', None),
                    'received_at': timezone.make_aware(datetime.datetime.combine(
                        line.get('date', None),
                        datetime.datetime.min.time()
                    )),
                    'sender_account_number': line.get('account_number', None),
                    'sender_bank': line.get('bank_code', None),
                    'sender_bic': line.get('bic', None),
                    'sender_iban': line.get('iban', None),
                    'specific_symbol': line.get('specific_symbol', None),
                    'user_identification': line.get('user_identification', None),
                    'variable_symbol': line.get('variable_symbol', None),
                    'scrape': scrape,
                },
            )
        scrape.status = SCRAPE_STATUS_SUCCESS
        scrape.save()
    except Exception as error:
        scrape.status = SCRAPE_STATUS_FAILURE
        scrape.save()
        raise error
