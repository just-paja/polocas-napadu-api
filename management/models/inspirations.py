from .base import BaseAdminModel


class InspirationAdmin(BaseAdminModel):
    """Admin model for inspirations."""
    list_display = ('show', 'text', 'discarded')
    list_filter = ('discarded',)
    search_fields = ('show.name', 'text')
