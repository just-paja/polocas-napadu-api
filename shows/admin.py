import re

from django.utils.translation import ugettext_lazy as _

from fields.admin import (
    BaseAdminModel,
    BaseInlineAdminModel,
    LocationFilter,
    SeasonFilter,
    ShowFilter,
    ShowTypeFilter,
)
from theatre_sports.models.match import Match

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

    def get_search_results(self, request, *args):
        """
        Filter results based on URL. If the URL corresponds to the URL of django
        admin for match edit, then filter show participants based on who is
        already mentioned in the show.
        """
        queryset, use_distinct = super().get_search_results(request, *args)
        referer = request.META.get('HTTP_REFERER', None)
        match_admin_url = '/theatre_sports/match/'
        if referer and match_admin_url in referer:
            match_id = re.search('/theatre_sports/match/([0-9]+)/change', referer)
            match = Match.objects.filter(pk=int(match_id[1])).first()
            if match:
                queryset = queryset.filter(show=match.show)
        return queryset, use_distinct

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


class ShowAdmin(BaseAdminModel):
    """Admin model for shows."""

    model = Show
    inlines = [
        ShowTicketPriceInlineAdmin,
        ShowParticipantInlineAdmin,
        ShowPhotoAdmin,
    ]
    autocomplete_fields = ["location", "sponsors"]
    list_display = ("name", "location", "start", "all_day", "visibility")
    list_filter = (EventSeasonFilter, ShowTypeFilter, LocationFilter, "visibility")
    search_fields = ("name", "all_day")
    readonly_fields = ("slug",)
    fieldsets = (
        (_("Identification"), {"fields": ("name", "slug", "show_type")}),
        (_("Date and time"), {"fields": ("start", "end", "all_day"), }),
        (_("Location"), {"fields": ("location", "description"), }),
        (_("Links"), {"fields": (
            "link_tickets",
            "link_reservations",
            "link_facebook",
            "email_reservations",
            "sponsors",
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
