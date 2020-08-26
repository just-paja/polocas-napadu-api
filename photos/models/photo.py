from django.db.models import PositiveIntegerField, TextField
from django_extensions.db.models import TimeStampedModel

from fields import VisibilityMixin
from images.fields import ImageField


class Photo(TimeStampedModel, VisibilityMixin):
    """Stores photos."""

    class Meta:
        abstract = True

    image = ImageField(
        height_field="height", width_field="width", upload_to="var/photos",
    )
    height = PositiveIntegerField(null=True, blank=True, editable=False, default=100,)
    width = PositiveIntegerField(null=True, blank=True, editable=False, default=100,)
    description = TextField(null=False, blank=True)
