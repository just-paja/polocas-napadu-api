from django.db.models import Model, ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _


class GameActor(Model):

    class Meta:
        verbose_name = _('Game Actor')
        verbose_name_plural = _('Game Actors')

    game = ForeignKey('Game', on_delete=CASCADE)
    participant = ForeignKey('shows.ShowParticipant', on_delete=CASCADE)
