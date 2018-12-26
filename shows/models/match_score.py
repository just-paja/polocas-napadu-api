from django.db.models import (
    Model,
    OneToOneField,
    PositiveIntegerField,
    PROTECT
)


class MatchScore(Model):
    results = OneToOneField(
        'MatchResults',
        on_delete=PROTECT,
        related_name='score',
    )
    show_band = OneToOneField(
        'ShowBand',
        on_delete=PROTECT,
        related_name='score',
    )
    score = PositiveIntegerField(default=0)
    penalty_points = PositiveIntegerField(default=0)
