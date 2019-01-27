from django.db.models import (
    Model,
    ManyToManyField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE
)
from django.utils.translation import ugettext_lazy as _

TEAM_HOME = 1
TEAM_GUEST = 2

TYPE_CHOICES = [
    (TEAM_HOME, _('team-home')),
    (TEAM_GUEST, _('team-guest')),
]

class ContestantGroup(Model):

    class Meta:
        verbose_name = _('Contestant Group')
        verbose_name_plural = _('Contestant Groups')

    contestant_type = PositiveIntegerField(
        choices=TYPE_CHOICES,
    )
    band = ForeignKey(
        'bands.Band',
        on_delete=CASCADE,
        related_name='contestant_groups',
    )
    match = ForeignKey(
        'Match',
        on_delete=CASCADE,
        related_name='contestant_groups',
    )
    players = ManyToManyField(
        'shows.ShowParticipant',
        related_name='contestant_groups',
    )

    def __str__(self):
        return self.band.name
