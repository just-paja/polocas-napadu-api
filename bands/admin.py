from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Band, BandPhoto


class BandPhotoAdmin(BaseInlineAdminModel):
    """Admin model for band photos."""

    model = BandPhoto


class BandAdmin(BaseAdminModel):
    """Admin model for bands."""

    model = Band
    inlines = [
        BandPhotoAdmin,
    ]
    list_display = ("name", "city", "website", "visibility")
    list_filter = ("visibility",)
    search_fields = ("name", "city")
