from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, Model, URLField

from fields import NameMixin, VisibilityMixin


class Band(TimeStampedModel, NameMixin, VisibilityMixin):
    city = CharField(max_length=127)
    website = URLField(blank=True, null=True)
