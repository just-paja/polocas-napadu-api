from django_extensions.db.models import TimeStampedModel
from django.db.models import BooleanField, OneToOneField, PROTECT

from events.models import Event


class MatchResults(TimeStampedModel):
    show = OneToOneField(
        'Show',
        on_delete=PROTECT,
        related_name='match_results',
    )
    closed = BooleanField(default=False)
