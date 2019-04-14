from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Game, GameActor, GameRules


class GameActorAdmin(BaseInlineAdminModel):

    model = GameActor


class GameAdmin(BaseAdminModel):

    model = Game
    inlines = [GameActorAdmin]


class GameRulesAdmin(BaseAdminModel):

    model = GameRules
