from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class BaseAdminModel(admin.ModelAdmin):
    pass


class BaseInlineAdminModel(admin.TabularInline):
    """Base admin for Inline models."""
    extra = 1


class BaseStackedAdminModel(admin.StackedInline):
    """Base admin for Inline models."""
    extra = 1


class LocationFilter(AutocompleteFilter):
    title = _('Location')
    field_name = 'location'


class ShowFilter(AutocompleteFilter):
    title = _('Show')
    field_name = 'show'
