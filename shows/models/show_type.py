from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, TextField

from fields import VisibilityManager, VisibilityMixin


class ShowTypeManager(VisibilityManager):
    pass


class ShowType(TimeStampedModel, VisibilityMixin):
    name = CharField(max_length=50)
    description = TextField()
    objects = ShowTypeManager()
