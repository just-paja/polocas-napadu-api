from django_extensions.db.models import TimeStampedModel

from .name import NameMixin
from .description import DescriptionMixin
from .visibility import VisibilityMixin

class PublicResourceMixin(
    TimeStampedModel,
    NameMixin,
    DescriptionMixin,
    VisibilityMixin
):
    class Meta:
        abstract = True
