from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, Model, TextField, URLField


class Location(TimeStampedModel):
    address = CharField(max_length=255)
    description = TextField()
    gps = CharField(max_length=127, blank=True, null=True)
    name = CharField(max_length=63)
    website = URLField(blank=True, null=True)
