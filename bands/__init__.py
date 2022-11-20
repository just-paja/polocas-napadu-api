from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BandsConfig(AppConfig):
    name = "bands"
    verbose_name = _("Bands")
