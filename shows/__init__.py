from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShowsConfig(AppConfig):
    name = "shows"
    verbose_name = _("Shows")
