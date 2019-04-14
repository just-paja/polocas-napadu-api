from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Location, LocationPhoto


class LocationPhotoAdmin(BaseInlineAdminModel):
    """Admin model for location photos."""

    model = LocationPhoto


class LocationAdmin(BaseAdminModel):
    """Admin model for locations."""

    model = Location
    inlines = [
        LocationPhotoAdmin,
    ]
    list_display = ('name', 'address', 'website', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('name', 'address')
