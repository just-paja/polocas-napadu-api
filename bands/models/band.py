from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, Model, URLField

from fields import VisibilityManager, VisibilityMixin


class BandManager(VisibilityManager):
    pass


class Band(TimeStampedModel, VisibilityMixin):
    name = CharField(max_length=127)
    city = CharField(max_length=127)
    website = URLField(blank=True, null=True)
    objects = BandManager()
