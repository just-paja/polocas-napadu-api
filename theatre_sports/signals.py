from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Match
from .schema import MatchSubscription

@receiver([post_save], sender=Match)
def propagate_match_change(sender, instance, **kwargs):
    MatchSubscription.update_match(instance)
