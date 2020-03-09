from django.utils.translation import ugettext_lazy as _

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
    ShowTicketPrice,
    ShowType,
    ShowTypePhoto,
    ShowVolumeCalibration,
    ShowVolumeCalibrationVoting,
)


class EventSeasonFilter(SeasonFilter):
    field = "start"


class ShowParticipantSeasonFilter(SeasonFilter):
    field = "show__start"


class ShowPhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowPhoto


class ShowTypePhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowTypePhoto


class ShowParticipantAdmin(BaseAdminModel):

    class Media:
        pass

    model = ShowParticipant
    list_display = (
        "profile",
        "get_role_name",
        "get_show_name",
        "get_show_date",
    )
    list_filter = (ShowParticipantSeasonFilter, ShowFilter, "role")
    search_fields = ["profile__name"]
    autocomplete_fields = [
        "show",
        "profile",
        "role",
    ]

    def get_role_name(self, item):
        return item.role.name

    def get_show_name(self, item):
        return item.show.name

    def get_show_date(self, item):
        return item.show.start

    get_role_name.admin_order_field = 'role__name'
    get_role_name.short_description = _("Role")
    get_show_date.admin_order_field = 'show__start'
    get_show_date.short_description = _("Date")
    get_show_name.short_description = _("Show")


class ShowParticipantInlineAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowParticipant
    autocomplete_fields = ["profile"]


class ShowTicketPriceInlineAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowTicketPrice
    search_fields = ('show__name', 'name')


class ShowAdmin(BaseAdminModel):
    """Admin model for shows."""

    model = Show
    inlines = [
        ShowTicketPriceInlineAdmin,
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
        (None, {"fields": ("sell_tickets", "capacity"), }),
        (None, {"fields": (
            "link_tickets",
            "link_reservations",
            "link_facebook",
            "email_reservations",
        ), }),
    )

    class Media:
        pass


class ShowRoleAdmin(BaseAdminModel):
    """Admin model for show roles."""

    model = ShowRole
    search_fields = ("name",)
    list_display = ('name', 'weight')
    ordering = ('weight',)


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
