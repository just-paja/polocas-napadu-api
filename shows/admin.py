from fields.admin import (
    BaseAdminModel,
    BaseInlineAdminModel,
    LocationFilter,
    SeasonFilter,
    ShowFilter,
    ShowTypeFilter,
)

from .models import (
    Show,
    ShowParticipant,
    ShowPhoto,
    ShowRole,
    ShowType,
    ShowTypePhoto,
    ShowVolumeCalibration,
    ShowVolumeCalibrationVoting,
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
    list_display = (
        "profile",
        "role",
        "get_show_name",
        "get_show_date",
    )
    list_filter = (ShowFilter, "role")
    search_fields = ["profile__name"]
    autocomplete_fields = [
        "show",
        "profile",
        "role",
    ]

    class Media:
        pass


class ShowParticipantInlineAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowParticipant
    autocomplete_fields = ["profile"]


class EventSeasonFilter(SeasonFilter):
    field = "start"


class ShowAdmin(BaseAdminModel):
    """Admin model for shows."""

    model = Show
    inlines = [
        ShowParticipantInlineAdmin,
        ShowPhotoAdmin,
    ]
    autocomplete_fields = ["location"]
    list_display = ("name", "location", "start", "all_day", "visibility")
    list_filter = (EventSeasonFilter, ShowTypeFilter, LocationFilter, "visibility")
    search_fields = ("name", "all_day")
    readonly_fields = ("slug",)
    fieldsets = (
        (None, {"fields": ("name", "slug", "show_type")}),
        (None, {"fields": ("start", "end", "all_day"), }),
        (None, {"fields": ("location", "description"), }),
        (None, {"fields": ("link_tickets", "link_reservations", "link_facebook"), }),
    )

    class Media:
        pass


class ShowRoleAdmin(BaseAdminModel):
    """Admin model for show roles."""

    model = ShowRole
    search_fields = ("name",)


class ShowTypeAdmin(BaseAdminModel):
    """Admin model for show types."""

    model = ShowType
    inlines = [
        ShowTypePhotoAdmin,
    ]
    fields = (
        "name",
        "slug",
        "visibility",
        "short_description",
        "description",
        "use_games",
        "use_fouls",
    )
    readonly_fields = ("slug",)
    list_display = ("name", "use_games", "use_fouls", "visibility")
    list_filter = ("use_games", "use_fouls", "visibility")
    search_fields = ("name",)


class ShowVolumeCalibrationAdmin(BaseAdminModel):

    model = ShowVolumeCalibration


class ShowVolumeCalibrationVotingAdmin(BaseAdminModel):

    model = ShowVolumeCalibrationVoting
