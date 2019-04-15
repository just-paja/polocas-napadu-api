from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _


class ShowParticipant(TimeStampedModel):

    class Meta:
        verbose_name = _('Show participant')
        verbose_name_plural = _('Show participants')

    show = ForeignKey(
        'Show',
        on_delete=CASCADE,
        related_name='showsParticipants',
    )
    profile = ForeignKey(
        'profiles.Profile',
        on_delete=CASCADE,
        related_name='showsParticipated',
    )
    role = ForeignKey(
        'ShowRole',
        on_delete=CASCADE,
        related_name='showsParticipants',
    )

    def __str__(self):
        return self.profile.name
