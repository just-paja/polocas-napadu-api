from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField


class ShowRole(TimeStampedModel):
    name = CharField(max_length=63)
