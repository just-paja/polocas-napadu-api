from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import gettext_lazy as _

from fields.admin import BaseAdminModel

from ..models import Purpose, PurposeCategory


class PurposeFilter(AutocompleteFilter):
    title = _("Purpose")
    field_name = "purpose"


class PurposeAdmin(BaseAdminModel):
    model = Purpose
    fields = ('name', 'description')
    list_display = (
        'id',
        'name',
        'get_promise_count',
    )
    list_filter = ()
    search_fields = ('name', 'description')


class PurposeCategoryAdmin(BaseAdminModel):
    model = PurposeCategory
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'purposes'),
        }),
    )
    list_display = (
        'id',
        'name',
    )
    list_filter = ()
