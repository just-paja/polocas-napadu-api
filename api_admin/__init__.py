from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApiAdminConfig(AppConfig):
    name = 'api_admin'
    verbose_name = _('Admin')
