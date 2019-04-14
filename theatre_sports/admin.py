from fields.admin import BaseAdminModel, BaseStackedAdminModel

from .models import (
    ContestantGroup,
    Foul,
    FoulType,
    Match,
    MatchStage,
    ScorePoint,
)


class FoulTypeAdmin(BaseAdminModel):

    model = FoulType


class FoulAdmin(BaseAdminModel):

    model = Foul


class ContestantGroupAdmin(BaseStackedAdminModel):

    model = ContestantGroup
    extra = 0


class ScorePointAdmin(BaseAdminModel):

    model = ScorePoint


class MatchStageAdmin(BaseAdminModel):

    model = MatchStage
    list_filter = ('match__show__name',)
    list_display = ('match', 'type', 'created')


class MatchAdmin(BaseAdminModel):

    model = Match
    change_form_template = 'admin/match_change_form.html'
    inlines = [
        ContestantGroupAdmin,
    ]
