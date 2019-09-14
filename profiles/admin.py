from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Profile, ProfileGroup, ProfilePhoto

class ProfileGroupAdmin(BaseAdminModel):
    """Admin model for profile groups."""

    model = ProfileGroup
    search_fields = ('name',)


class ProfilePhotoAdmin(BaseInlineAdminModel):
    """Admin model for profile photos."""

    model = ProfilePhoto


class ProfileAdmin(BaseAdminModel):
    """Admin model for profiles."""

    model = Profile
    inlines = [
        ProfilePhotoAdmin,
    ]
    fields = ('name', 'alias', 'group', 'visibility', 'about')
    list_display = ('name', 'alias', 'group', 'visibility')
    list_filter = ('group', 'visibility')
    search_fields = ('name', 'alias')
