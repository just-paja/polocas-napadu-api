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
    list_display = ('name', 'address', 'website', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('name', 'address')
