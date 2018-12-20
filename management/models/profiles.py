from profiles.models import ProfilePhoto

from .base import BaseAdminModel, BaseInlineAdminModel


class ProfilePhotoAdmin(BaseInlineAdminModel):
    """Admin model for profile photos."""

    model = ProfilePhoto


class ProfileAdmin(BaseAdminModel):
    """Admin model for profiles."""
    inlines = [
        ProfilePhotoAdmin,
    ]
    search_fields = ('name',)
