from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import admin as auth_admin

from admin_sso.admin import AssignmentAdmin
from admin_sso.models import Assignment

from bands.models import Band
from games.models import Game, GameRules
from inspirations.models import Inspiration
from locations.models import Location
from profiles.models import Profile, ProfileGroup
from shows.models import Show, ShowRole, ShowType
from gsuite.views import gauth
from theatre_sports.models import (
    Foul,
    FoulType,
    Match,
    MatchStage,
    ScorePoint
)

from .models import (
    BandAdmin,
    FoulAdmin,
    FoulTypeAdmin,
    InspirationAdmin,
    LocationAdmin,
    GameAdmin,
    GameRulesAdmin,
    MatchAdmin,
    MatchStageAdmin,
    ProfileAdmin,
    ProfileGroupAdmin,
    ScorePointAdmin,
    ShowAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
)


class ImprovAdminSite(AdminSite):
    site_header = 'Poločas nápadu'

    def __init__(self, name='admin'):
        super(ImprovAdminSite, self).__init__(name)
        if settings.DJANGO_ADMIN_SSO:
            self.login = gauth


ADMIN_SITE = ImprovAdminSite()

ADMIN_SITE.register(Band, BandAdmin)
ADMIN_SITE.register(Foul, FoulAdmin)
ADMIN_SITE.register(FoulType, FoulTypeAdmin)
ADMIN_SITE.register(Game, GameAdmin)
ADMIN_SITE.register(GameRules, GameRulesAdmin)
ADMIN_SITE.register(Inspiration, InspirationAdmin)
ADMIN_SITE.register(Location, LocationAdmin)
ADMIN_SITE.register(Match, MatchAdmin)
ADMIN_SITE.register(MatchStage, MatchStageAdmin)
ADMIN_SITE.register(Profile, ProfileAdmin)
ADMIN_SITE.register(ProfileGroup, ProfileGroupAdmin)
ADMIN_SITE.register(ScorePoint, ScorePointAdmin)
ADMIN_SITE.register(Show, ShowAdmin)
ADMIN_SITE.register(ShowRole, ShowRoleAdmin)
ADMIN_SITE.register(ShowType, ShowTypeAdmin)

ADMIN_SITE.register(auth_admin.Group, auth_admin.GroupAdmin)
ADMIN_SITE.register(auth_admin.User, auth_admin.UserAdmin)
ADMIN_SITE.register(Assignment, AssignmentAdmin)
