from graphene import Field, List, String

from graphene_django.types import DjangoObjectType

from .models import GameActor, GameRules, Game


class GameActorNode(DjangoObjectType):
    class Meta:
        model = GameActor


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
    game = Field(GameNode)
    game_list = List(GameNode)
    game_rules = Field(GameRulesNode, slug=String())
    game_rules_list = List(GameRulesNode)

    def resolve_game_list(self, info):
        return Game.objects.filter(show__visible=True).all()

    def resolve_game_rules(self, info, slug=None):
        try:
            return GameRules.objects.get_visible().get(slug=slug)
        except GameRules.DoesNotExist:
            return None

    def resolve_game_rules_list(self, info):
        return GameRules.objects.get_visible().all()
