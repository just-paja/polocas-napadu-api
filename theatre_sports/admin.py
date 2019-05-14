from fields.admin import BaseAdminModel, BaseStackedAdminModel

from .models import (
    ContestantGroup,
    Foul,
    FoulType,
    Match,
    MatchStage,
    ScorePoint,
    ScorePointPoll,
    ScorePointPollVoting,
)


class FoulTypeAdmin(BaseAdminModel):

    model = FoulType
    search_fields = ['name', 'description']
    list_display = ['name', 'visibility']


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
    list_display = [
        'band',
        'get_color_block',
        'contestant_type',
        'get_show_name',
        'get_show_date',
    ]
    list_filter = ['contestant_type']
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
    list_display = [
        'get_contestant_group_name',
        'get_score_snapshot',
        'get_game_name',
        'get_show_name',
        'get_show_date',
    ]


class ScorePointPollVotingInlineAdmin(BaseStackedAdminModel):

    model = ScorePointPollVoting


class ScorePointPollAdmin(BaseAdminModel):

    model = ScorePointPoll
    inlines = [ScorePointPollVotingInlineAdmin]
    list_display = ('pk', 'poll_type', 'match', 'game', 'winner')


class MatchStageAdmin(BaseAdminModel):

    model = MatchStage
    list_filter = ('match__show__name',)
    list_display = (
        'show',
        'type',
        'get_game_name',
        'get_duration',
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
    list_display = [
        'get_show_name',
        'get_show_date',
        'closed',
        'get_current_stage_name',
    ]
    autocomplete_fields = ['show']
    search_fields = [
        'show__name',
        'show__start',
        'show__location__name',
    ]
