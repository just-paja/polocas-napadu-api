from fields.admin import BaseAdminModel
from .models import LivePollVoting, VolumeScrape


class LivePollVotingAdmin(BaseAdminModel):

    model = LivePollVoting
    list_display = ("pk", "closed", "vote_type", "avg_volume")


class VolumeScrapeAdmin(BaseAdminModel):

    model = VolumeScrape
    list_display = ("pk", "volume")
