from django.utils.translation import ugettext_lazy as _

from fields.admin import (
    BaseAdminModel,
    BaseInlineAdminModel,
    LocationFilter,
    SeasonFilter,
)
from ..models import Event, EventParticipant, EventTicketPrice


class EventSeasonFilter(SeasonFilter):
    field = "start"


class EventParticipantInlineAdmin(BaseInlineAdminModel):
    model = EventParticipant
    autocomplete_fields = ["profile"]


class EventTicketPriceInlineAdmin(BaseInlineAdminModel):
    model = EventTicketPrice


class EventViewerAdmin(BaseAdminModel):
    model = Event
    search_fields = ("name", "all_day")
    list_display = ("name", "location", "start", "all_day", "canceled", "visibility")
    readonly_fields = (
        "all_day",
        "description",
        "email_reservations",
        "end",
        "link_facebook",
        "link_reservations",
        "link_tickets",
        "location",
        "name",
        "slug",
        "sponsors",
        "start",
        "visibility",
    )


class EventAdmin(BaseAdminModel):
    model = Event
    inlines = (
        EventTicketPriceInlineAdmin,
        EventParticipantInlineAdmin,
    )
    autocomplete_fields = ["location", "sponsors"]
    list_display = ("name", "location", "start", "visibility", "all_day", "canceled")
    list_filter = (EventSeasonFilter, LocationFilter, "visibility", "canceled")
    search_fields = ("name", "all_day")
    readonly_fields = ("slug",)
    fieldsets = (
        (_("Identification"), {"fields": ("name", "slug", "description")}),
        (_("Date and time"), {"fields": ("location", "start", "end", "all_day")}),
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
