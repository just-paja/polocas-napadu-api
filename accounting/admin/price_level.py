from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import ugettext_lazy as _

from fields.admin import BaseAdminModel

from ..models import PriceLevel


class PriceLevelAdmin(BaseAdminModel):
    model = PriceLevel
    fields = ('name', 'description', 'is_default', 'weight')
    list_display = (
        'name',
        'is_default',
        'weight',
        'modified',
    )
    ordering = ('weight',)
    list_filter = ()
    search_fields = ('name', 'description')
