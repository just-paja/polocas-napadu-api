from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VotingConfig(AppConfig):
    name = "voting"
    verbose_name = _("Voting")
