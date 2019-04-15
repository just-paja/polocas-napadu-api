"""Import Django models."""
from django.db.models import ImageField, PositiveIntegerField
from django_extensions.db.models import TimeStampedModel

from fields import DescriptionMixin, VisibilityMixin


class Photo(
    TimeStampedModel,
    DescriptionMixin,
    VisibilityMixin
):
    """Stores photos."""

    class Meta:
        """Defines photo as abstract class."""

        abstract = True

    image = ImageField(
        height_field="height",
        width_field="width",
        upload_to='var/photos',
    )
    height = PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
        default=100,
    )
    width = PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
        default=100,
    )
