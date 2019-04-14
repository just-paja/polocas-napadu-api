from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import (
    Show,
    ShowRole,
    ShowType,
    ShowBand,
    ShowParticipant,
    ShowPhoto,
    ShowTypePhoto,
)


class ShowPhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowPhoto


class ShowTypePhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowTypePhoto


class ShowParticipantAdmin(BaseAdminModel):
    """Admin model for show photos."""

    model = ShowParticipant
    search_fields = ['profile__name']


class ShowParticipantInlineAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowParticipant
    autocomplete_fields = ['profile']


class ShowBandAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowBand


class ShowAdmin(BaseAdminModel):
    """Admin model for shows."""

    model = Show
    inlines = [
        ShowParticipantInlineAdmin,
        ShowPhotoAdmin,
    ]
    autocomplete_fields = ['location']
    list_display = ('name', 'location', 'start', 'all_day', 'visibility')
    list_filter = ('location', 'visibility',)
    search_fields = ('name', 'all_day')
    fieldsets = (
        (None, {
            'fields': ('name', 'show_type')
        }),
        (None, {
            'fields': ('start', 'end', 'all_day'),
        }),
        (None, {
            'fields': ('location', 'description'),
        })
    )


class ShowRoleAdmin(BaseAdminModel):
    """Admin model for show roles."""

    model = ShowRole
    search_fields = ('name',)


class ShowTypeAdmin(BaseAdminModel):
    """Admin model for show types."""

    model = ShowType
    inlines = [
        ShowTypePhotoAdmin,
    ]
    list_display = ('name', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('name',)
