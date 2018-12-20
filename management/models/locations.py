from locations.models import LocationPhoto

from .base import BaseAdminModel, BaseInlineAdminModel


class LocationPhotoAdmin(BaseInlineAdminModel):
    """Admin model for location photos."""

    model = LocationPhoto


class LocationAdmin(BaseAdminModel):
    """Admin model for locations."""
    inlines = [
        LocationPhotoAdmin,
    ]
    search_fields = ('name',)
