from graphene import DateTime, Int, Field, Float, List, ObjectType, Mutation
from graphene_django.types import DjangoObjectType

from fields import is_staff
from .models import VolumeScrape, LivePollVoting


class VolumeScrapeNode(DjangoObjectType):
    class Meta:
        model = VolumeScrape


class LivePollVotingNode(DjangoObjectType):
    class Meta:
        model = LivePollVoting


class Query:
    volume_scrape_list = List(
        VolumeScrapeNode, live_poll_voting_id=Int(), last_scrape=DateTime(),
    )

    def resolve_volume_scrape_list(self, info, **kwargs):
        try:
            voting = LivePollVoting.objects.get(pk=kwargs.get("live_poll_voting_id"))
        except LivePollVoting.DoesNotExist:
            return []
        source = voting.volume_scrapes
        last_scrape = kwargs.get("last_scrape")
        if last_scrape:
            source = source.filter(created__gt=last_scrape)
        return source.all()


class ScrapeStageVolume(Mutation):
    class Arguments:
        live_poll_voting_id = Int(required=True)
        volume = Float(required=True)

    volume_scrape = Field(lambda: VolumeScrapeNode)

    @staticmethod
    @is_staff
    def mutate(root, info, live_poll_voting_id, volume):
        voting = LivePollVoting.objects.get(pk=live_poll_voting_id)
        volume_scrape = VolumeScrape(voting=voting, volume=volume,)
        volume_scrape.clean()
        volume_scrape.save()
        return ScrapeStageVolume(volume_scrape=volume_scrape)


class CloseLivePollVoting(Mutation):
    class Arguments:
        live_poll_voting_id = Int(required=True)

    live_poll_voting = Field(lambda: LivePollVotingNode)

    @staticmethod
    @is_staff
    def mutate(root, info, live_poll_voting_id):
        voting = LivePollVoting.objects.get(pk=live_poll_voting_id)
        voting.close()
        return CloseLivePollVoting(live_poll_voting=voting)


class Mutations(ObjectType):
    scrape_stage_volume = ScrapeStageVolume.Field()
    close_live_poll_voting = CloseLivePollVoting.Field()
