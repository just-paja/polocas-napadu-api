from django.utils.translation import ugettext_lazy as _

from events.admin import EventAdmin
from fields.admin import BaseInlineAdminModel

from ..models import Workshop, WorkshopPhoto


class WorkshopPhotoAdmin(BaseInlineAdminModel):
    model = WorkshopPhoto


class WorkshopAdmin(EventAdmin):
    model = Workshop
    inlines = EventAdmin.inlines + (
        WorkshopPhotoAdmin,
    )
    fieldsets = (
        (_("Identification"), {"fields": ("name", "slug", "description")}),
        (_("Date and time"), {"fields": (
            "location",
            "start",
            "end",
            "all_day",
            "canceled",
            "capacity",
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
