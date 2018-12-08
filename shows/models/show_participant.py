from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, CASCADE


class ShowParticipant(TimeStampedModel):
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
