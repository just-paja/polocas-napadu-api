"""Import Django models."""
from django.db.models import CharField, ImageField, PositiveIntegerField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from fields import VisibilityManager, VisibilityMixin


class PhotoManager(VisibilityManager):
    pass


class Photo(TimeStampedModel, VisibilityMixin):
    """Stores photos."""

    class Meta:
        """Defines photo as abstract class."""

        abstract = True

    objects = PhotoManager()
    image = ImageField(
        height_field="height",
        width_field="width",
        upload_to='var/photos',
    )
    height = PositiveIntegerField(null=True, blank=True, editable=False, default=100)
    width = PositiveIntegerField(null=True, blank=True, editable=False, default=100)
    description = CharField(
        verbose_name=_("Description"),
        max_length=255,
        null=True,
        blank=True,
    )
