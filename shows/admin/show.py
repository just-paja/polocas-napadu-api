from django.utils.translation import ugettext_lazy as _

from events.admin import EventAdmin
from fields.admin import (
    BaseInlineAdminModel,
    SeasonFilter,
    ShowTypeFilter,
)
from ..models import Show, ShowPhoto


class EventSeasonFilter(SeasonFilter):
    field = "start"


class ShowPhotoAdmin(BaseInlineAdminModel):
    """Admin model for show photos."""

    model = ShowPhoto


class ShowAdmin(EventAdmin):
    """Admin model for shows."""

    model = Show
    inlines = EventAdmin.inlines + (
        ShowPhotoAdmin,
    )
    list_filter = EventAdmin.list_filter + (ShowTypeFilter,)
    fieldsets = (
        (_("Identification"), {"fields": ("name", "slug", "show_type", "description")}),
        (_("Date and time"), {"fields": (
            "location",
            "start",
            "end",
            "use_inspirations",
            "all_day",
            "canceled",
        )}),
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
