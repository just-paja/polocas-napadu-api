import datetime

from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from fields.admin import BaseAdminModel, IntValueFilter, empty_value

ACTIVE_YES = 1
ACTIVE_NO = 2

ACTIVE_CHOICES = (
    (ACTIVE_YES, _('Yes')),
    (ACTIVE_NO, _('No')),
)


class TimeLimitedActiveFilter(IntValueFilter):
    title = _('Active')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return ACTIVE_CHOICES

    def queryset(self, request, queryset):
        today = datetime.date.today()
        filter_value = self.value()
        if filter_value == ACTIVE_YES:
            return queryset.filter(
                Q(end__isnull=True) | Q(end__gt=today)
            ).filter(
                Q(start__isnull=True) | Q(start__lte=today)
            )
        if filter_value == ACTIVE_NO:
            return queryset.filter(
                Q(start__lt=today, end__isnull=False, end__lt=today) |
                Q(start__gt=today),
                start__isnull=False,
            )
        return queryset


class TimeLimitedAdmin(BaseAdminModel):

    def format_start(self, item):
        return item.start or empty_value('-∞')

    def format_end(self, item):
        return item.end or empty_value('∞')

    def changelist_view(self, request, extra_context=None):
        has_questionmark = '?' in request.META.get('HTTP_REFERER', '')
        has_param = 'active' in request.GET
        if has_questionmark or has_param:
            return super().changelist_view(request, extra_context)
        return redirect('%s?active=1' % request.get_full_path())

    format_end.admin_order_field = 'end'
    format_end.short_description = _('End')
    format_start.admin_order_field = 'start'
    format_start.short_description = _('Start')
