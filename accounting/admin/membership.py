from fields.admin import BaseAdminModel, BaseInlineAdminModel

from ..models import Membership, MembershipFee, MembershipLevel, MembershipLevelFee


class MembershipLevelFeeAdmin(BaseInlineAdminModel):
    model = MembershipLevelFee
    fields = ('amount', 'currency', 'start', 'end')
    extra = 0


class MembershipLevelAdmin(BaseAdminModel):
    model = MembershipLevel
    search_fields = ('name', 'description')
    list_display = ('name', 'is_active', 'start', 'end')
    inlines = (MembershipLevelFeeAdmin,)
    fields = ('name', 'description', 'start', 'end', 'created', 'modified')
    readonly_fields = ('modified', 'created')


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
    model = Membership
    search_fields = ('user__first_name', 'user__last_name')
    autocomplete_fields = ('user',)
    list_display = ('user', 'level', 'is_active', 'start', 'end')
    fields = ('user', 'level', 'start', 'end', 'created', 'modified')
    readonly_fields = ('modified', 'created')
