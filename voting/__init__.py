from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VotingConfig(AppConfig):
    name = "voting"
    verbose_name = _("Voting")
