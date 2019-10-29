from fields.admin import BaseAdminModel, ShowFilter

from .models import Reservation


class ReservationAdmin(BaseAdminModel):
    model = Reservation
    fields = (
        'show',
        'status',
        'customer_name',
        'customer_email',
        'seat_count',
        'seat_location',
        'newsletter',
        'created',
        'modified',
    )
    autocomplete_fields = ['show']
    list_display = ('customer_name', 'customer_email', 'seat_count', 'status', 'created', 'show')
    list_filter = (ShowFilter, 'status', 'newsletter')
    readonly_fields = ('created', 'modified')
    search_fields = ('customer_name', 'customer_email')
    ordering = ('-created',)

    class Media:
        pass
