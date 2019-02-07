from django.db.models import (
    Model,
    ManyToManyField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE
)
from django.utils.translation import ugettext_lazy as _
from colorfield.fields import ColorField

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
    color = ColorField(default='#ccc')
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

    def get_other_side(self):
        if self.contestant_type == TEAM_HOME:
            return TEAM_GUEST
        if self.contestant_type == TEAM_GUEST:
            return TEAM_HOME
        return None

    def get_foes(self):
        other_side = self.get_other_side()
        if other_side:
            return self.match.contestant_groups.filter(contestant_type=other_side)
        return []

    def get_penalty_points(self):
        return self.fouls.count() % 3

    def get_penalty_points_addition(self):
        total = 0
        foes = self.get_foes()
        for foe in foes:
            total += foe.fouls.count() // 3
        return total
