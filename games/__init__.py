from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GamesConfig(AppConfig):
    name = 'games'
    verbose_name = _('Games')
