from theatre_sports.models import ContestantGroup

from .base import BaseAdminModel, BaseStackedAdminModel


class FoulTypeAdmin(BaseAdminModel):
    pass


class FoulAdmin(BaseAdminModel):
    pass


class ContestantGroupAdmin(BaseStackedAdminModel):
    model = ContestantGroup
    extra = 0


class ScorePointAdmin(BaseAdminModel):
    pass


class MatchStageAdmin(BaseAdminModel):
    list_filter = ('match__show__name',)
    list_display = ('match', 'type', 'created')


class MatchAdmin(BaseAdminModel):
    change_form_template = 'admin/match_change_form.html'
    inlines = [
        ContestantGroupAdmin,
    ]
