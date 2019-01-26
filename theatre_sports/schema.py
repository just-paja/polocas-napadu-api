from graphene import Int, Field, List, Node

from graphene_django.types import DjangoObjectType
from fields import VISIBILITY_PUBLIC

from .models import ContestantGroup, Foul, Match, MatchStage, ScorePoint


class ContestantGroupNode(DjangoObjectType):
    class Meta:
        model = ContestantGroup


class FoulNode(DjangoObjectType):
    class Meta:
        model = Foul


class MatchStageNode(DjangoObjectType):
    class Meta:
        model = MatchStage


class MatchNode(DjangoObjectType):
    class Meta:
        model = Match

    current_stage = Field(MatchStageNode)

    def resolve_current_stage(self, info):
        return self.stages.order_by('-created').first()


class ScorePointNode(DjangoObjectType):
    class Meta:
        model = ScorePoint


class Query:
    match = Field(MatchNode, id=Int())
    match_list = List(MatchNode)

    def resolve_match(self, info, **kwargs):
        return Match.objects.get(pk=kwargs.get('id'))

    def resolve_match_list(self, info):
        return Match.objects.filter(show__visibility=VISIBILITY_PUBLIC).all()
