from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Game, GameActor, GameRules


class GameActorAdmin(BaseInlineAdminModel):

    model = GameActor


class GameAdmin(BaseAdminModel):

    model = Game
    inlines = [GameActorAdmin]
    search_fields = [
        'rules__name',
    ]


class GameRulesAdmin(BaseAdminModel):

    model = GameRules
