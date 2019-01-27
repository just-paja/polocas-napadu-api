from games.models import GameActor

from .base import BaseAdminModel, BaseInlineAdminModel


class GameActorAdmin(BaseInlineAdminModel):
    model = GameActor


class GameAdmin(BaseAdminModel):
    inlines = [GameActorAdmin]


class GameRulesAdmin(BaseAdminModel):
    pass
