from admin_auto_filters.filters import AutocompleteFilter

from django.utils.translation import ugettext_lazy as _
from fields.admin import BaseInlineAdminModel

from ..models import Membership, MembershipFee, MembershipLevel, MembershipLevelFee
from .time_limited import TimeLimitedAdmin, TimeLimitedActiveFilter


class MembershipLevelFeeAdmin(BaseInlineAdminModel):
    model = MembershipLevelFee
    fields = ('amount', 'currency', 'start', 'end')
    extra = 0


class MembershipLevelAdmin(TimeLimitedAdmin):
    model = MembershipLevel
    search_fields = ('name', 'description')
    list_filter = (TimeLimitedActiveFilter,)
    list_display = ('name', 'is_active', 'format_start', 'format_end')
    inlines = (MembershipLevelFeeAdmin,)
    fields = ('name', 'description', 'start', 'end', 'created', 'modified')
    readonly_fields = ('modified', 'created')


class MembershipLevelFilter(AutocompleteFilter):
    title = _("Level")
    field_name = "level"


class MemberFilter(AutocompleteFilter):
    title = _("Member")
    field_name = "user"


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


class MembershipAdmin(TimeLimitedAdmin):
    class Media:
        pass

    model = Membership
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    autocomplete_fields = ('user',)
    list_filter = (
        MembershipLevelFilter,
        MemberFilter,
        TimeLimitedActiveFilter
    )
    list_display = ('user', 'level', 'is_active', 'format_start', 'format_end')
    fields = ('user', 'level', 'start', 'end', 'created', 'modified')
    readonly_fields = ('modified', 'created')
