from django.db.models import BooleanField, Model, OneToOneField, PROTECT

from events.models import Event


class MatchResults(Model):
    show = OneToOneField(
        'Show',
        on_delete=PROTECT,
        related_name='match_results',
    )
    closed = BooleanField(default=False)
