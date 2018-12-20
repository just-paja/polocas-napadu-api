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
    search_fields = ('name',)
