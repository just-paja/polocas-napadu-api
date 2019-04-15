from fields.admin import BaseAdminModel

from .models import Inspiration

class InspirationAdmin(BaseAdminModel):
    """Admin model for inspirations."""

    model = Inspiration
    list_display = ('show', 'text', 'discarded')
    list_filter = ('discarded',)
    search_fields = ('show__name', 'text')
    autocomplete_fields = ['show']
