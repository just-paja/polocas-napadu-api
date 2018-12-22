from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, TextField

from fields import NameMixin, VisibilityMixin


class ShowType(NameMixin, TimeStampedModel, VisibilityMixin):
    description = TextField()
