from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import GameActor, GameInspiration, GameRules, Game


class GameActorNode(DjangoObjectType):
    class Meta:
        model = GameActor


class GameInspirationNode(DjangoObjectType):
    class Meta:
        model = GameInspiration


class GameRulesNode(DjangoObjectType):
    class Meta:
        model = GameRules


class GameNode(DjangoObjectType):
    class Meta:
        model = Game


class Query:
    get_game = relay.Node.Field(GameNode)
    get_game_rules = relay.Node.Field(GameRulesNode)
    list_game = List(GameNode)
    list_game_rules = List(GameRulesNode)

    def resolve_list_games(self, info):
        return Game.objects.filter(show__visible=True).all()

    def resolve_list_game_rules(self, info):
        return GameRules.objects.get_visible().all()
