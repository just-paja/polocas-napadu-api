from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, TextField


class ShowType(TimeStampedModel):
    name = CharField(max_length=50)
    description = TextField()
