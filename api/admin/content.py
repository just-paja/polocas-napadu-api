from django.utils.translation import gettext_lazy as _

from admin_sso.admin import AssignmentAdmin
from admin_sso.models import Assignment

from blog.admin import ArticleAdmin, ChapterAdmin, PoemAdmin
from bands.admin import BandAdmin
from events.admin import MODELS as EVENTS
from fields.admin import ImprovAdminSite
from games.admin import GameAdmin, GameRulesAdmin
from inspirations.admin import InspirationAdmin
from locations.admin import LocationAdmin, UsualPlaceAdmin
from profiles.admin import ProfileAdmin, ProfileGroupAdmin, SponsorAdmin
from shows.admin import MODELS as SHOWS
from workshops.admin import MODELS as WORKSHOPS
from theatre_sports.admin import (
    ContestantGroupAdmin,
    FoulAdmin,
    FoulTypeAdmin,
    MatchAdmin,
    MatchStageAdmin,
    ScorePointAdmin,
)
from tickets.admin import ReservationAdmin


class ContentAdminSite(ImprovAdminSite):
    name = 'content'
    site_title = _('Content admin')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookup(ArticleAdmin)
        self.hookup_all(EVENTS)
        self.hookup_all(SHOWS)
        self.hookup_all(WORKSHOPS)
        self.hookup(BandAdmin)
        self.hookup(ContestantGroupAdmin)
        self.hookup(FoulAdmin)
        self.hookup(FoulTypeAdmin)
        self.hookup(GameAdmin)
        self.hookup(GameRulesAdmin)
        self.hookup(ChapterAdmin)
        self.hookup(InspirationAdmin)
        self.hookup(LocationAdmin)
        self.hookup(MatchAdmin)
        self.hookup(MatchStageAdmin)
        self.hookup(PoemAdmin)
        self.hookup(ProfileAdmin)
        self.hookup(ProfileGroupAdmin)
        self.hookup(ReservationAdmin)
        self.hookup(ScorePointAdmin)
        self.hookup(SponsorAdmin)
        self.hookup(UsualPlaceAdmin)
        self.register(Assignment, AssignmentAdmin)
