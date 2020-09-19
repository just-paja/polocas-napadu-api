from fields.admin import BaseAdminModel, ShowFilter

from events.admin import EventFilter

from ..models import Reservation


class ReservationAdmin(BaseAdminModel):
    model = Reservation
    fields = (
        "event",
        "status",
        "customer_name",
        "customer_email",
        "seat_count",
        "seat_location",
        "newsletter",
        "created",
        "modified",
    )
    autocomplete_fields = ["event"]
    list_display = (
        "customer_name",
        "customer_email",
        "seat_count",
        "status",
        "created",
        "event",
    )
    list_filter = (EventFilter, "status", "newsletter")
    readonly_fields = ("created", "modified")
    search_fields = ("customer_name", "customer_email")
    ordering = ("-created",)

    class Media:
        pass
