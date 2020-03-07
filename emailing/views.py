from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import render


def test_email_template(request):
    return render(request, 'membership/thanks_for_payment.html', {
        'amount_diff': '50 CZK',
        'amount': '300 CZK',
        'date': now(),
        'membership_days': 333,
        'organization_name': settings.ORGANIZATION_NAME,
        'organization_name_from': settings.ORGANIZATION_NAME_FROM,
        'organization_name_formal': settings.ORGANIZATION_NAME_FORMAL,
        'sender_name': 'Karel z Poločasu nápadu',
        'underpaid': False,
        'overpaid': False,
        'variable_symbol': 123123,
    })
