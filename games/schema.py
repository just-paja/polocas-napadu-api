from graphene import List, Node, String

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
    type = String()

    class Meta:
        model = Game

    def resolve_type(self, info):
        return self.rules.name


class Query:
    game = Node.Field(GameNode)
    game_list = List(GameNode)
    game_rules = Node.Field(GameRulesNode)
    game_rules_list = List(GameRulesNode)

    def resolve_game_list(self, info):
        return Game.objects.filter(show__visible=True).all()

    def resolve_game_rules_list(self, info):
        return GameRules.objects.get_visible().all()
