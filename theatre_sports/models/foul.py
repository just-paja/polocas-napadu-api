from django.db.models import TextField, ForeignKey, CASCADE, PROTECT
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Foul(TimeStampedModel):
    class Meta:
        verbose_name = _("Foul")
        verbose_name_plural = _("Fouls")

    contestant_group = ForeignKey(
        "ContestantGroup",
        on_delete=CASCADE,
        related_name="fouls",
        verbose_name=_("Contestant"),
    )
    game = ForeignKey(
        "games.Game",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="fouls",
        verbose_name=_("Game"),
    )
    player = ForeignKey(
        "events.EventParticipant",
        blank=True,
        null=True,
        on_delete=CASCADE,
        related_name="fouls",
        verbose_name=_("Player"),
    )
    foul_type = ForeignKey(
        "FoulType",
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="fouls",
        verbose_name=_("Foul type"),
    )
    comment = TextField(
        blank=True,
        verbose_name=_("Comment"),
        help_text=_("Describe what was the foul play"),
    )

    def __str__(self):
        if self.foul_type:
            return "%s, %s" % (
                self.foul_type.name,
                self.player or self.contestant_group,
            )
        return "Foul#%s" % self.pk

    def get_time(self):
        if (
            not self.created
            or not self.contestant_group
            or not self.contestant_group.match
        ):
            return None
        start = self.contestant_group.match.get_actual_start()
        return self.created - start


Foul.get_time.short_description = _("Match time")
