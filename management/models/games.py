from games.models import GameActor, GameInspiration

from .base import BaseAdminModel, BaseInlineAdminModel


class GameActorAdmin(BaseInlineAdminModel):
    model = GameActor


class GameInspirationAdmin(BaseInlineAdminModel):
    model = GameInspiration


class GameAdmin(BaseAdminModel):
    inlines = [GameActorAdmin, GameInspirationAdmin]


class GameRulesAdmin(BaseAdminModel):
    pass
