from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import admin as auth_admin

from admin_sso.admin import AssignmentAdmin
from admin_sso.models import Assignment

from bands.admin import BandAdmin
from games.admin import GameAdmin, GameRulesAdmin
from inspirations.admin import InspirationAdmin
from locations.admin import LocationAdmin
from profiles.admin import ProfileAdmin, ProfileGroupAdmin
from gsuite.views import gauth
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
    ScorePointAdmin
)


class ImprovAdminSite(AdminSite):
    site_header = 'Poločas nápadu'

    def __init__(self, name='admin'):
        super(ImprovAdminSite, self).__init__(name)
        if settings.DJANGO_ADMIN_SSO:
            self.login = gauth


ADMIN_SITE = ImprovAdminSite()

ADMIN_SITE.register(BandAdmin.model, BandAdmin)
ADMIN_SITE.register(ContestantGroupAdmin.model, ContestantGroupAdmin)
ADMIN_SITE.register(FoulAdmin.model, FoulAdmin)
ADMIN_SITE.register(FoulTypeAdmin.model, FoulTypeAdmin)
ADMIN_SITE.register(GameAdmin.model, GameAdmin)
ADMIN_SITE.register(GameRulesAdmin.model, GameRulesAdmin)
ADMIN_SITE.register(InspirationAdmin.model, InspirationAdmin)
ADMIN_SITE.register(LocationAdmin.model, LocationAdmin)
ADMIN_SITE.register(MatchAdmin.model, MatchAdmin)
ADMIN_SITE.register(MatchStageAdmin.model, MatchStageAdmin)
ADMIN_SITE.register(ProfileAdmin.model, ProfileAdmin)
ADMIN_SITE.register(ProfileGroupAdmin.model, ProfileGroupAdmin)
ADMIN_SITE.register(ScorePointAdmin.model, ScorePointAdmin)
ADMIN_SITE.register(ShowAdmin.model, ShowAdmin)
ADMIN_SITE.register(ShowParticipantAdmin.model, ShowParticipantAdmin)
ADMIN_SITE.register(ShowRoleAdmin.model, ShowRoleAdmin)
ADMIN_SITE.register(ShowTypeAdmin.model, ShowTypeAdmin)

ADMIN_SITE.register(auth_admin.Group, auth_admin.GroupAdmin)
ADMIN_SITE.register(auth_admin.User, auth_admin.UserAdmin)
ADMIN_SITE.register(Assignment, AssignmentAdmin)
