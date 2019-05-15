from graphene import Int, List
from graphene_django.types import DjangoObjectType

from .models import VolumeScrape, LivePollVoting

class VolumeScrapeNode(DjangoObjectType):
    class Meta:
        model = VolumeScrape


class Query:
    volume_scrape_list = List(
        VolumeScrapeNode,
        live_poll_voting_id=Int(),
    )

    def resolve_volume_scrape_list(self, info, **kwargs):
        try:
            voting = LivePollVoting.objects.get(pk=kwargs.get('live_poll_voting_id'))
        except LivePollVoting.DoesNotExist:
            return []

        return voting.volume_scrapes.all()
