import datetime
from admin_auto_filters.filters import AutocompleteFilter

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import SimpleListFilter
from django.db.models import Q
from fields.admin import BaseAdminModel, BaseInlineAdminModel

from ..models import Membership, MembershipFee, MembershipLevel, MembershipLevelFee


ACTIVE_YES = 1
ACTIVE_NO = 2

ACTIVE_CHOICES = (
    (ACTIVE_YES, _('Yes')),
    (ACTIVE_NO, _('No')),
)


class TimeLimitedActiveFilter(SimpleListFilter):
    title = _('Active')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return ACTIVE_CHOICES

    def queryset(self, request, queryset):
        today = datetime.date.today()
        try:
            filter_value = int(self.value())
        except TypeError:
            filter_value = None
        if filter_value == ACTIVE_YES:
            return queryset.filter(Q(end__isnull=True) | Q(end__gt=today), start__lte=today)
        if filter_value == ACTIVE_NO:
            return queryset.filter(
                Q(start__lt=today, end__isnull=False, end__lt=today) |
                Q(start__gt=today)
            )
        return queryset


class MembershipLevelFeeAdmin(BaseInlineAdminModel):
    model = MembershipLevelFee
    fields = ('amount', 'currency', 'start', 'end')
    extra = 0


class MembershipLevelAdmin(BaseAdminModel):
    model = MembershipLevel
    search_fields = ('name', 'description')
    list_filter = (TimeLimitedActiveFilter,)
    list_display = ('name', 'is_active', 'start', 'end')
    inlines = (MembershipLevelFeeAdmin,)
    fields = ('name', 'description', 'start', 'end', 'created', 'modified')
    readonly_fields = ('modified', 'created')


class MembershipLeveFilter(AutocompleteFilter):
    title = _("Level")
    field_name = "level"


class MembershipFeeAdmin(BaseInlineAdminModel):
    model = MembershipFee
    fieldsets = (
        (None, {
            'fields': ('level_fee', 'start', 'end'),
        }),
    )
    list_display = (
        'name',
        'amount',
        'get_volume_price_tag',
        'modified'
    )
    search_fields = (
        'membership__user__first_name',
        'membership__user__last_name',
        'purpose__name'
    )
    autocomplete_fields = ('membership',)


class MembershipAdmin(BaseAdminModel):
    class Media:
        pass

    model = Membership
    search_fields = ('user__first_name', 'user__last_name')
    autocomplete_fields = ('user',)
    list_filter = (MembershipLeveFilter, TimeLimitedActiveFilter)
    list_display = ('user', 'level', 'is_active', 'start', 'end')
    fields = ('user', 'level', 'start', 'end', 'created', 'modified')
    readonly_fields = ('modified', 'created')
