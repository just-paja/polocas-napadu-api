from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from events.admin import EventViewerAdmin
from fields.admin import ImprovAdminSite

from .reservation import ReservationAdmin


class TicketsAdminSite(ImprovAdminSite):
    name = 'tickets'
    site_title = _('Tickets')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookup(EventViewerAdmin)
        self.hookup(ReservationAdmin)
        self.register(auth_admin.User, auth_admin.UserAdmin)


TICKETS_ADMIN = TicketsAdminSite()
