from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, Model, TextField, URLField

from fields import NameMixin, VisibilityManager, VisibilityMixin


class Location(NameMixin, TimeStampedModel, VisibilityMixin):
    description = TextField()
    address = CharField(max_length=255)
    gps = CharField(max_length=127, blank=True, null=True)
    website = URLField(blank=True, null=True)
