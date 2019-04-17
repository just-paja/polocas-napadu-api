from fields.admin import BaseAdminModel, BaseInlineAdminModel, ShowFilter

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
    list_display = [
        'rules',
        'get_show_name',
        'get_show_date',
        'modified',
    ]
    list_filter = [ShowFilter]
    search_fields = [
        'rules__name',
    ]

    class Media:
        pass


class GameRulesAdmin(BaseAdminModel):

    model = GameRules
    search_fields = [
        'name',
        'description',
    ]
    list_display = [
        'name',
        'visibility',
        'modified',
    ]
