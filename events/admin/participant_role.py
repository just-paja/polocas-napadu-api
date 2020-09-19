from fields.admin import BaseAdminModel

from ..models import ParticipantRole


class ParticipantRoleAdmin(BaseAdminModel):
    model = ParticipantRole
    search_fields = ("name",)
    list_display = ('name', 'weight')
    ordering = ('weight',)
