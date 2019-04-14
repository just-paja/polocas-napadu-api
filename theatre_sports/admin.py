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
    search_fields = ['name', 'description']


class FoulAdmin(BaseAdminModel):

    model = Foul
    search_fields = ['foul__name', 'foul__description']
    autocomplete_fields = [
        'contestant_group',
        'foul_type',
        'game',
        'player',
    ]


class ContestantGroupAdmin(BaseAdminModel):

    model = ContestantGroup
    search_fields = [
        'band__name',
        'contestant_type',
        'match__show__name',
    ]


class ContestantGroupInlineAdmin(BaseStackedAdminModel):

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
        ContestantGroupInlineAdmin,
    ]
