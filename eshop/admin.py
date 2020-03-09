from fields.admin import BaseAdminModel
from shows.models import ShowTicketPrice

from .models import ShowTicket


class ShowTicketPriceAdmin(BaseAdminModel):

    model = ShowTicketPrice
    search_fields = ('show__name', 'name')


class ShowTicketAdmin(BaseAdminModel):

    model = ShowTicket

    autocomplete_fields = ('show_ticket_price',)
    fields = ('show_ticket_price', 'price', 'currency')
    list_display = (
        'show_ticket_price',
        'price',
        'currency',
        'used_on',
        'created'
    )
