from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, Model, URLField


class Band(TimeStampedModel):
    name = CharField(max_length=127)
    city = CharField(max_length=127)
    website = URLField(blank=True, null=True)
