from django.contrib import admin


class BaseAdminModel(admin.ModelAdmin):
    pass


class BaseInlineAdminModel(admin.TabularInline):
    """Base admin for Inline models."""
    extra = 1


class BaseStackedAdminModel(admin.StackedInline):
    """Base admin for Inline models."""
    extra = 1
