from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import ugettext_lazy as _
import nested_admin


class BaseAdminModel(nested_admin.NestedModelAdmin):
    pass


class BaseInlineAdminModel(nested_admin.NestedTabularInline):
    """Base admin for Inline models."""
    extra = 1


class BaseStackedAdminModel(nested_admin.NestedStackedInline):
    """Base admin for Inline models."""
    extra = 1


class LocationFilter(AutocompleteFilter):
    title = _('Location')
    field_name = 'location'


class ShowFilter(AutocompleteFilter):
    title = _('Show')
    field_name = 'show'


class ShowTypeFilter(AutocompleteFilter):
    title = _('Show type')
    field_name = 'show_type'
