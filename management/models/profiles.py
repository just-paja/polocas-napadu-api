from profiles.models import ProfilePhoto

from .base import BaseAdminModel, BaseInlineAdminModel


class ProfileGroupAdmin(BaseAdminModel):
    """Admin model for profile groups."""

    search_fields = ('name',)


class ProfilePhotoAdmin(BaseInlineAdminModel):
    """Admin model for profile photos."""

    model = ProfilePhoto


class ProfileAdmin(BaseAdminModel):
    """Admin model for profiles."""
    inlines = [
        ProfilePhotoAdmin,
    ]
    list_display = ('name', 'group', 'visibility')
    list_filter = ('group', 'visibility')
    search_fields = ('name',)
