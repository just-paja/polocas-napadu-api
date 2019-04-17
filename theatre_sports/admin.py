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
    list_display = [
        'foul_type',
        'contestant_group',
        'player',
        'game',
    ]
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
    autocomplete_fields = [
        'band',
        'match',
        'players',
    ]


class ContestantGroupInlineAdmin(BaseStackedAdminModel):

    model = ContestantGroup
    extra = 0
    autocomplete_fields = [
        'band',
        'players',
    ]


class ScorePointAdmin(BaseAdminModel):

    model = ScorePoint
    autocomplete_fields = [
        'contestant_group',
        'game',
    ]


class MatchStageAdmin(BaseAdminModel):

    model = MatchStage
    list_filter = ('match__show__name',)
    list_display = (
        'show',
        'type',
        'game_name',
        'duration',
        'created'
    )
    autocomplete_fields = [
        'game',
        'match',
        'inspirations',
    ]


class MatchAdmin(BaseAdminModel):

    model = Match
    change_form_template = 'admin/match_change_form.html'
    inlines = [
        ContestantGroupInlineAdmin,
    ]
    autocomplete_fields = ['show']
    search_fields = [
        'show__name',
        'show__start',
        'show__location__name',
    ]
