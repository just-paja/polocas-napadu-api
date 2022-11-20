from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountingConfig(AppConfig):
    name = 'accounting'
    verbose_name = _('Accounting')
