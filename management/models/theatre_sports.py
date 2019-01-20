from theatre_sports.models import (
    ContestantGroup,
    ScorePoint,
)

from .base import BaseAdminModel, BaseInlineAdminModel


class FoulTypeAdmin(BaseAdminModel):
    pass


class FoulAdmin(BaseAdminModel):
    pass


class ContestantGroupAdmin(BaseInlineAdminModel):

    model = ContestantGroup


class ScorePointAdmin(BaseAdminModel):
    pass


class MatchStageAdmin(BaseAdminModel):
    list_filter = ('match__show__name',)
    list_display = ('match', 'type', 'created')


class MatchAdmin(BaseAdminModel):

    inlines = [
        ContestantGroupAdmin,
    ]
