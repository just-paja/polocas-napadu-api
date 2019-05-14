from fields.admin import BaseAdminModel
from .models import LivePollVoting, VolumeScrape


class LivePollVotingAdmin(BaseAdminModel):

    model = LivePollVoting
    list_display = ('pk', 'vote_type')


class VolumeScrapeAdmin(BaseAdminModel):

    model = VolumeScrape
    list_display = ('pk', 'volume')
