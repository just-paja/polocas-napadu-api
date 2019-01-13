from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import ContestantGroup, Foul, Match, ScorePoint


class ContestantGroupNode(DjangoObjectType):
    class Meta:
        model = ContestantGroup


class FoulNode(DjangoObjectType):
    class Meta:
        model = Foul


class MatchNode(DjangoObjectType):
    class Meta:
        model = Match


class ScorePointNode(DjangoObjectType):
    class Meta:
        model = ScorePoint


class Query:
    get_match = relay.Node.Field(MatchNode)
    list_matches = List(MatchNode)

    def resolve_list_inspirations(self, info):
        return Match.objects.filter(show__visible=True).all()
