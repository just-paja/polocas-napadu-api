from bands.models import BandPhoto

from .base import BaseAdminModel, BaseInlineAdminModel


class BandPhotoAdmin(BaseInlineAdminModel):
    """Admin model for band photos."""

    model = BandPhoto


class BandAdmin(BaseAdminModel):
    """Admin model for bands."""
    inlines = [
        BandPhotoAdmin,
    ]
    list_display = ('name', 'city', 'website', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('name', 'city')
