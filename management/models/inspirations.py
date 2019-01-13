from locations.models import LocationPhoto

from .base import BaseAdminModel, BaseInlineAdminModel


class InspirationAdmin(BaseAdminModel):
    """Admin model for inspirations."""
    list_display = ('show', 'text', 'discarded')
    list_filter = ('discarded',)
    search_fields = ('show.name', 'text')
