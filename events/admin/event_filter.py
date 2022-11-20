from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import gettext_lazy as _


class EventFilter(AutocompleteFilter):
    title = _("Event")
    field_name = "event"
