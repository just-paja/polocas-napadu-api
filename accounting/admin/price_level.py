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
    search_fields = ('name', 'description')
