from shows.models import (
    ShowBand,
    ShowParticipant,
    ShowPhoto,
    ShowTypePhoto,
)

from .base import BaseAdminModel, BaseInlineAdminModel


class ShowPhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowPhoto


class ShowTypePhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowTypePhoto


class ShowParticipantAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowParticipant


class ShowBandAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowBand


class ShowAdmin(BaseAdminModel):
    """Admin model for shows."""

    inlines = [
        ShowParticipantAdmin,
        ShowPhotoAdmin,
    ]
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

    search_fields = ('name',)


class ShowTypeAdmin(BaseAdminModel):
    """Admin model for show types."""

    inlines = [
        ShowTypePhotoAdmin,
    ]
    list_display = ('name', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('name',)
