from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmailingConfig(AppConfig):
    name = "emailing"
    verbose_name = _("Emailing")
