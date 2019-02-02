from graphene import Boolean, Int, Field, List, String, ObjectType, Mutation

from graphene_django.types import DjangoObjectType
from fields import append_host_from_context, VISIBILITY_PUBLIC
from games.models import Game

from .models import ContestantGroup, Foul, Match, MatchStage, ScorePoint


class ContestantGroupNode(DjangoObjectType):
    class Meta:
        model = ContestantGroup

    logo = String()
    score = Int()

    def resolve_logo(self, info):
        if not self.band.logo:
            return None
        return append_host_from_context(self.band.logo.url, info.context)

    def resolve_score(self, info):
        return self.score_points.count()


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
    prev_stage = Field(MatchStageNode)

    def resolve_current_stage(self, info):
        return self.get_current_stage()

    def resolve_prev_stage(self, info):
        try:
            return self.stages.order_by('-created')[1]
        except IndexError:
            return None


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


def check_auth(args, pred):
    _, info = args
    if not pred(info.context):
        raise Exception("Unauthorized")


def is_staff(func):
    def wrapper(*args, **kwargs):
        check_auth(args, lambda context: context.user.is_staff)
        return func(*args, **kwargs)
    return wrapper


class ChangeMatchStage(Mutation):
    class Arguments:
        game_id = Int()
        match_id = Int(required=True)
        stage = String(required=True)

    stage = Field(MatchStageNode)
    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, match_id=None, stage=None, game_id=None):
        match = Match.objects.get(pk=match_id)
        game = Game.objects.get(pk=game_id) if game_id else None
        stage = MatchStage.objects.create(
            game=game,
            match=match,
            type=int(stage.split('_')[1]),
        )
        return ChangeMatchStage(
            stage=stage,
            ok=True
        )


class RewindMatchStage(Mutation):
    class Arguments:
        match_id = Int(required=True)

    stage = Field(MatchStageNode)
    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, match_id=None):
        match = Match.objects.get(pk=match_id)
        current_stage = match.get_current_stage()
        current_stage.delete()
        return ChangeMatchStage(
            stage=match.get_current_stage(),
            ok=True
        )


class Mutations(ObjectType):
    changeMatchStage = ChangeMatchStage.Field()
    rewindMatchStage = RewindMatchStage.Field()
