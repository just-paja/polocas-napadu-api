from django.db.models import (
    Model,
    ManyToManyField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE,
)
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from colorfield.fields import ColorField

TEAM_HOME = 1
TEAM_GUEST = 2

TYPE_CHOICES = [
    (TEAM_HOME, _("team-home")),
    (TEAM_GUEST, _("team-guest")),
]


class ContestantGroup(Model):
    class Meta:
        verbose_name = _("Contestant Group")
        verbose_name_plural = _("Contestant Groups")

    contestant_type = PositiveIntegerField(
        choices=TYPE_CHOICES, verbose_name=_("Contestant Type"),
    )
    band = ForeignKey(
        "bands.Band",
        on_delete=CASCADE,
        related_name="contestant_groups",
        verbose_name=_("Band"),
    )
    color = ColorField(default="#ccc", verbose_name=_("Color"),)
    match = ForeignKey(
        "Match",
        on_delete=CASCADE,
        related_name="contestant_groups",
        verbose_name=_("Match"),
    )
    players = ManyToManyField(
        "shows.ShowParticipant",
        related_name="contestant_groups",
        verbose_name=_("Players"),
    )

    def __str__(self):
        return self.band.name

    def get_show_name(self):
        return self.match.get_show_name()

    def get_show_date(self):
        return self.match.get_show_date()

    def get_color_block(self):
        return mark_safe(
            """
            <div
                style="
                    background: %s;
                    width: 3rem;
                    height: 1rem
                "
            ></div>
        """
            % (self.color)
        )

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


ContestantGroup.get_color_block.short_description = _("Color")
ContestantGroup.get_show_date.short_description = _("Date")
ContestantGroup.get_show_name.short_description = _("Match")
