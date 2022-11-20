import re

from django.utils.translation import gettext_lazy as _
from fields.admin import BaseAdminModel, SeasonFilter
from theatre_sports.models import Match

from .event_filter import EventFilter

from ..models import EventParticipant


class EventParticipantSeasonFilter(SeasonFilter):
    field = "event__start"


class EventParticipantAdmin(BaseAdminModel):

    class Media:
        pass

    model = EventParticipant
    list_display = (
        "profile",
        "get_role_name",
        "get_event_name",
        "get_event_date",
    )
    list_filter = (EventParticipantSeasonFilter, EventFilter, "role")
    search_fields = ["profile__name"]
    autocomplete_fields = [
        "event",
        "profile",
    ]

    def get_search_results(self, request, *args):
        """
        Filter results based on URL. If the URL corresponds to the URL of django
        admin for match edit, then filter event participants based on who is
        already mentioned in the event.
        """
        queryset, use_distinct = super().get_search_results(request, *args)
        referer = request.META.get('HTTP_REFERER', None)
        match_admin_url = '/theatre_sports/match/'
        if referer and match_admin_url in referer:
            match_id = re.search('/theatre_sports/match/([0-9]+)/change', referer)
            if match_id:
                match = Match.objects.filter(pk=int(match_id[1])).first()
                if match:
                    queryset = queryset.filter(event=match.show)
        return queryset, use_distinct

    def get_role_name(self, item):
        return item.role.name

    def get_event_name(self, item):
        return item.event.name

    def get_event_date(self, item):
        return item.event.start

    get_role_name.admin_order_field = 'role__name'
    get_role_name.short_description = _("Role")
    get_event_date.admin_order_field = 'event__start'
    get_event_date.short_description = _("Date")
    get_event_name.short_description = _("Event")
