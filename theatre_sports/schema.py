from graphene import Boolean, Int, Field, List, String, ObjectType, Mutation

from graphene_django.types import DjangoObjectType
from fields import append_host_from_context, VISIBILITY_PUBLIC

from games.models import Game, GameRules
from games.schema import GameNode
from inspirations.models import Inspiration
from inspirations.schema import InspirationNode

from .models import ContestantGroup, Foul, Match, MatchStage, ScorePoint


class ContestantGroupNode(DjangoObjectType):
    class Meta:
        model = ContestantGroup

    logo = String()
    score = Int()
    penalty_points = Int()

    def resolve_logo(self, info):
        if not self.band.logo:
            return None
        return append_host_from_context(self.band.logo.url, info.context)

    def resolve_score(self, info):
        return self.score_points.count()

    def resolve_penalty_points(self, info):
        return self.fouls.count()


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
    prepared_inspiration_count = Int()

    def resolve_current_stage(self, info):
        return self.get_current_stage()

    def resolve_prev_stage(self, info):
        return self.get_prev_stage()

    def resolve_prepared_inspiration_count(self, info):
        return self.show.inspirations.filter(
            discarded=False,
            stages=None,
        ).count()


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
        match_id = Int(required=True)
        stage = String(required=True)

    stage = Field(MatchStageNode)
    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, match_id=None, stage=None):
        match = Match.objects.get(pk=match_id)
        prev_stage = match.get_current_stage()
        stage_type = int(stage.split('_')[1])
        if prev_stage and prev_stage.pass_game_to_next_stage():
            stage = MatchStage.objects.create(
                game=prev_stage.game,
                match=match,
                type=stage_type,
            )
            stage.inspirations.set(prev_stage.inspirations.all())
            prev_stage.game.inspirations.set(prev_stage.inspirations.all())
        else:
            stage = MatchStage.objects.create(
                match=match,
                type=stage_type,
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


class SetMatchGame(Mutation):
    class Arguments:
        match_id = Int(required=True)
        game_rules_id = Int(required=False)

    game = Field(GameNode)
    stage = Field(MatchStageNode)
    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, match_id, game_rules_id=None):
        match = Match.objects.get(pk=match_id)
        stage = match.get_current_stage()
        if game_rules_id:
            rules = GameRules.objects.get(pk=game_rules_id)
            if stage.game:
                stage.game.rules = rules
                stage.game.save()
            else:
                game = Game.objects.create(
                    show=match.show,
                    rules=rules,
                )
                stage.game = game
                stage.save()
        elif stage.game:
            game = stage.game
            stage.game = None
            stage.save()
            game.delete()
        return SetMatchGame(
            game=stage.game,
            stage=stage,
            ok=True
        )


class RandomPickInspiration(Mutation):
    class Arguments:
        replace = Boolean()
        match_id = Int(required=True)

    stage = Field(MatchStageNode)
    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, match_id, replace=False):
        match = Match.objects.get(pk=match_id)
        stage = match.get_current_stage()
        inspiration = None
        if replace:
            for insp in stage.inspirations.all():
                insp.discarded = True
                insp.save()
            stage.inspirations.clear()
            stage.save()
        inspiration = match.show.inspirations.filter(
            discarded=False,
            stages=None,
        ).order_by('?').first()
        if inspiration:
            stage.inspirations.add(inspiration)
            stage.save()
        return RandomPickInspiration(
            stage=stage,
            ok=True
        )


class DiscardInspiration(Mutation):
    class Arguments:
        inspiration_id = Int(required=True)

    inspiration = Field(InspirationNode)
    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, inspiration_id):
        inspiration = Inspiration.objects.get(pk=inspiration_id)
        if inspiration:
            inspiration.discarded = True
            inspiration.stages.clear()
            inspiration.save()
        return DiscardInspiration(
            inspiration=inspiration,
            ok=True
        )


class Mutations(ObjectType):
    discard_inspiration = DiscardInspiration.Field()
    change_match_stage = ChangeMatchStage.Field()
    random_pick_inspiration = RandomPickInspiration.Field()
    rewind_match_stage = RewindMatchStage.Field()
    set_match_game = SetMatchGame.Field()
