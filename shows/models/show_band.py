from django.db.models import CASCADE, Model, ForeignKey, PositiveIntegerField
from django.utils.translation import ugettext_lazy as _

TEAM_HOME = 1
TEAM_GUEST = 2

TYPE_CHOICES = [
    (TEAM_HOME, _('team-home')),
    (TEAM_HOME, _('team-guest')),
]

class ShowBand(Model):
    show = ForeignKey(
        'Show',
        related_name='show_band',
        on_delete=CASCADE,
    )
    band = ForeignKey(
        'bands.Band',
        related_name='bands',
        on_delete=CASCADE,
    )
    type = PositiveIntegerField(choices=TYPE_CHOICES)
