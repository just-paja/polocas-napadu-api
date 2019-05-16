from django.db.models import BooleanField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .live_poll_type_field import LivePollTypeField


class LivePollVoting(TimeStampedModel):
    vote_type = LivePollTypeField()
    closed = BooleanField(
        default=False,
        verbose_name=_('Closed'),
    )

    class Meta:
        verbose_name = _('Live Poll Voting')
        verbose_name_plural = _('Live Poll Votings')

    class AlreadyClosed(ValidationError):
        pass
