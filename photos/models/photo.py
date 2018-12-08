"""Import Django models."""
from django.db.models import CharField, ImageField, PositiveIntegerField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

VISIBILITY_PRIVATE = 1
VISIBILITY_PUBLIC = 2
VISIBILITY_DELETED = 3

VISIBILITY_CHOICES = (
    (VISIBILITY_PRIVATE, 'Private'),
    (VISIBILITY_PUBLIC, 'Public'),
    (VISIBILITY_DELETED, 'Deleted'),
)

class Photo(TimeStampedModel):
    """Stores photos."""

    class Meta:
        """Defines photo as abstract class."""

        abstract = True

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
    visibility = PositiveIntegerField(
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
    )
