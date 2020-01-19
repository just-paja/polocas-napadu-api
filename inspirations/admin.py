from fields.admin import BaseAdminModel, ShowFilter

from .models import Inspiration


class InspirationAdmin(BaseAdminModel):
    """Admin model for inspirations."""

    model = Inspiration
    list_display = ("text", "get_show_name", "get_show_date", "discarded")
    list_filter = (ShowFilter, "discarded")
    search_fields = ("show__name", "text")
    autocomplete_fields = ["show"]

    class Media:
        pass
