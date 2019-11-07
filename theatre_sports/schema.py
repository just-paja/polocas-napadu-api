from graphene import Boolean, Int, Field, List, String, ObjectType, Mutation

from graphene_django.types import DjangoObjectType
from fields import append_host_from_context, is_staff, VISIBILITY_PUBLIC

from games.models import Game, GameRules
from games.schema import GameNode
from inspirations.models import Inspiration
from inspirations.schema import InspirationNode
from voting.schema import VolumeScrapeNode

from .models import (
    ContestantGroup,
    Foul,
    FoulType,
    Match,
    MatchStage,
    ScorePoint,
    ScorePointPoll,
    ScorePointPollVoting,
)


class ContestantGroupNode(DjangoObjectType):
    class Meta:
        model = ContestantGroup

    logo = String()
    score = Int()
    score_points = Int()
    penalty_points = Int()

    def resolve_logo(self, info):
        if not self.band.logo:
            return None
        return append_host_from_context(self.band.logo.url, info.context)

    def resolve_score(self, info):
        return self.score_points.count() + self.get_penalty_points_addition()

    def resolve_score_points(self, info):
        return self.score_points.count()

    def resolve_penalty_points(self, info):
        return self.get_penalty_points()


class FoulTypeNode(DjangoObjectType):
    class Meta:
        model = FoulType


class FoulNode(DjangoObjectType):
    class Meta:
        model = Foul


class MatchStageNode(DjangoObjectType):
    class Meta:
        model = MatchStage


class ScorePointNode(DjangoObjectType):
    class Meta:
        model = ScorePoint


class MatchNode(DjangoObjectType):
    class Meta:
        model = Match

    current_stage = Field(MatchStageNode)
    prev_stage = Field(MatchStageNode)
    prepared_inspiration_count = Int()
    score_points = List(ScorePointNode)

    def resolve_current_stage(self, info):
        return self.get_current_stage()

    def resolve_prev_stage(self, info):
        return self.get_prev_stage()

    def resolve_prepared_inspiration_count(self, info):
        return self.show.inspirations.filter(
            discarded=False,
            stages=None,
            inspiration_games=None,
        ).count()

    def resolve_score_points(self, info):
        return ScorePoint.objects.filter(game__show__match__id=self.id)


class ScorePointPollNode(DjangoObjectType):
    class Meta:
        model = ScorePointPoll


class ScorePointPollVotingNode(DjangoObjectType):
    volume_scrapes = List(VolumeScrapeNode)

    class Meta:
        model = ScorePointPollVoting

    def resolve_volume_scrapes(self, info):
        return self.volume_scrapes.all()


class Query:
    foul_type_list = List(FoulTypeNode)
    match = Field(MatchNode, id=Int())
    match_list = List(MatchNode)
    score_point_poll = Field(ScorePointPollNode, match_stage_id=Int())

    def resolve_foul_type_list(self, info, **kwargs):
        return FoulType.objects.all()

    def resolve_match(self, info, **kwargs):
        try:
            return Match.objects.get(pk=kwargs.get('id'))
        except Match.DoesNotExist:
            return None

    def resolve_match_list(self, info):
        return Match.objects.filter(show__visibility=VISIBILITY_PUBLIC).all()

    def resolve_score_point_poll(self, info, **kwargs):
        try:
            stage = MatchStage.objects.get(pk=kwargs.get('match_stage_id'))
        except MatchStage.DoesNotExist:
            return None
        try:
            return stage.score_point_poll
        except ScorePointPoll.DoesNotExist:
            return None


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
        game = None
        inspirations = []
        if prev_stage and prev_stage.pass_game_to_next_stage():
            game = prev_stage.game
            inspirations = prev_stage.inspirations.all()
            if inspirations:
                game.inspirations.set(inspirations)
        stage = MatchStage.objects.create(
            game=game,
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
            inspiration_games=None,
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


class ChangeContestantGroupScore(Mutation):
    class Arguments:
        contestant_group_id = Int(required=True)
        subtract = Boolean()

    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, contestant_group_id, subtract=False):
        group = ContestantGroup.objects.get(pk=contestant_group_id)
        game = group.match.get_current_game()
        success = False
        if game and group:
            if subtract:
                score_point = ScorePoint.objects.filter(contestant_group=group).last()
                success = True
                if score_point:
                    score_point.delete()
            else:
                ScorePoint.objects.create(
                    game=game,
                    contestant_group=group,
                )
            success = True
        return DiscardInspiration(ok=success)


class AddFoulPoint(Mutation):
    class Arguments:
        contestant_group_id = Int(required=True)
        foul_type_id = Int(required=True)
        player_id = Int()

    ok = Boolean()

    @staticmethod
    @is_staff
    def mutate(root, info, contestant_group_id, foul_type_id, player_id=None):
        group = ContestantGroup.objects.get(pk=contestant_group_id)
        foul_type = FoulType.objects.get(pk=foul_type_id)
        game = group.match.get_current_game()
        result = False
        if player_id:
            player = group.players.get(pk=player_id)
        else:
            player = None
        if group and foul_type:
            Foul.objects.create(
                contestant_group=group,
                game=game,
                player=player,
                foul_type=foul_type,
            )
            result = True
        return AddFoulPoint(ok=result)


class AddAndUseInspiration(Mutation):
    class Arguments:
        match_id = Int(required=True)
        inspiration_text = String(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, match_id, inspiration_text):
        match = Match.objects.get(pk=match_id)
        stage = match.get_current_stage()
        inspiration = Inspiration.objects.create(
            show=match.show,
            text=inspiration_text,
        )
        stage.inspirations.add(inspiration)
        return AddAndUseInspiration(ok=True)


class StartScorePointVoting(Mutation):
    class Arguments:
        contestant_group_id = Int(required=True)

    voting = Field(lambda: ScorePointPollVotingNode)

    @staticmethod
    @is_staff
    def mutate(root, info, contestant_group_id):
        contestant_group = ContestantGroup.objects.get(pk=contestant_group_id)
        match = contestant_group.match

        if match.closed:
            return StartScorePointVoting()

        stage = match.get_current_stage()

        if not stage.can_vote_on_score_points():
            return StartScorePointVoting()

        try:
            poll = ScorePointPoll.objects.get(stage=stage)
        except ScorePointPoll.DoesNotExist:
            poll = ScorePointPoll.objects.create(stage=stage)

        try:
            voting = poll.votings.get(contestant_group=contestant_group_id)
            voting.closed = False
            voting.save()
            voting.volume_scrapes.all().delete()
        except ScorePointPollVoting.DoesNotExist:
            voting = ScorePointPollVoting.objects.create(
                poll=poll,
                contestant_group=contestant_group,
            )
        return StartScorePointVoting(voting=voting)


class CloseScorePointPoll(Mutation):
    class Arguments:
        score_point_poll_id = Int(required=True)

    score_point_poll = Field(lambda: ScorePointPollNode)

    @staticmethod
    @is_staff
    def mutate(root, info, score_point_poll_id):
        voting = ScorePointPoll.objects.get(pk=score_point_poll_id)
        voting.winner = voting.get_winning_option()
        voting.closed = True
        voting.save()
        return CloseScorePointPoll(score_point_poll=voting)


class Mutations(ObjectType):
    add_and_use_inspiration = AddAndUseInspiration.Field()
    add_foul_point = AddFoulPoint.Field()
    close_score_point_poll = CloseScorePointPoll.Field()
    discard_inspiration = DiscardInspiration.Field()
    change_contestant_group_score = ChangeContestantGroupScore.Field()
    change_match_stage = ChangeMatchStage.Field()
    random_pick_inspiration = RandomPickInspiration.Field()
    rewind_match_stage = RewindMatchStage.Field()
    set_match_game = SetMatchGame.Field()
    start_score_point_voting = StartScorePointVoting.Field()
