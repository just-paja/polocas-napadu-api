from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, Model, TextField, URLField

from fields import VisibilityManager, VisibilityMixin


class LocationManager(VisibilityManager):
    pass


class Location(TimeStampedModel, VisibilityMixin):
    name = CharField(max_length=63)
    description = TextField()
    address = CharField(max_length=255)
    gps = CharField(max_length=127, blank=True, null=True)
    website = URLField(blank=True, null=True)
    objects = LocationManager();
