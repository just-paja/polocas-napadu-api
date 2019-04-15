from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Game, GameActor, GameRules


class GameActorAdmin(BaseInlineAdminModel):

    model = GameActor
    autocomplete_fields = [
        'participant',
    ]


class GameAdmin(BaseAdminModel):

    model = Game
    inlines = [GameActorAdmin]
    autocomplete_fields = [
        'show',
        'rules',
        'inspirations',
    ]
    search_fields = [
        'rules__name',
    ]


class GameRulesAdmin(BaseAdminModel):

    model = GameRules
    search_fields = [
        'name',
        'description',
    ]
