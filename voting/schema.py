from graphene import DateTime, Int, List
from graphene_django.types import DjangoObjectType

from .models import VolumeScrape, LivePollVoting

class VolumeScrapeNode(DjangoObjectType):
    class Meta:
        model = VolumeScrape


class Query:
    volume_scrape_list = List(
        VolumeScrapeNode,
        live_poll_voting_id=Int(),
        last_scrape=DateTime(),
    )

    def resolve_volume_scrape_list(self, info, **kwargs):
        try:
            voting = LivePollVoting.objects.get(pk=kwargs.get('live_poll_voting_id'))
        except LivePollVoting.DoesNotExist:
            return []
        source = voting.volume_scrapes
        last_scrape = kwargs.get('last_scrape')
        if last_scrape:
            source = source.filter(created__gt=last_scrape)
        return source.all()
