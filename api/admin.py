from django.contrib.auth import admin as auth_admin

from admin_sso.admin import AssignmentAdmin
from admin_sso.models import Assignment

from blog.admin import ArticleAdmin, ChapterAdmin, PoemAdmin
from bands.admin import BandAdmin
from fields.admin import ImprovAdminSite
from games.admin import GameAdmin, GameRulesAdmin
from inspirations.admin import InspirationAdmin
from locations.admin import LocationAdmin, UsualPlaceAdmin
from profiles.admin import ProfileAdmin, ProfileGroupAdmin
from shows.admin import (
    ShowAdmin,
    ShowParticipantAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookup(ArticleAdmin)
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
        self.hookup(ShowAdmin)
        self.hookup(ShowParticipantAdmin)
        self.hookup(ShowRoleAdmin)
        self.hookup(ShowTypeAdmin)
        self.hookup(UsualPlaceAdmin)


class ConfigurationAdminSite(ImprovAdminSite):
    name = 'configuration'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(auth_admin.Group, auth_admin.GroupAdmin)
        self.register(auth_admin.User, auth_admin.UserAdmin)
        self.register(Assignment, AssignmentAdmin)


CONTENT_ADMIN = ContentAdminSite()
CONFIGURATION_ADMIN = ConfigurationAdminSite()
