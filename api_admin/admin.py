from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import admin as auth_admin

from admin_sso.admin import AssignmentAdmin
from admin_sso.models import Assignment

from blog.admin import ArticleAdmin, ChapterAdmin, PoemAdmin
from bands.admin import BandAdmin
from games.admin import GameAdmin, GameRulesAdmin
from inspirations.admin import InspirationAdmin
from locations.admin import LocationAdmin, UsualPlaceAdmin
from profiles.admin import ProfileAdmin, ProfileGroupAdmin
from gsuite.views import gauth
from shows.admin import (
    ShowAdmin,
    ShowParticipantAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
    ShowVolumeCalibrationAdmin,
    ShowVolumeCalibrationVotingAdmin,
)
from theatre_sports.admin import (
    ContestantGroupAdmin,
    FoulAdmin,
    FoulTypeAdmin,
    MatchAdmin,
    MatchStageAdmin,
    ScorePointAdmin,
    ScorePointPollAdmin,
)
from tickets.admin import ReservationAdmin
from voting.admin import (
    LivePollVotingAdmin,
    VolumeScrapeAdmin,
)


class ImprovAdminSite(AdminSite):
    site_header = 'Poločas nápadu'

    def __init__(self, name='admin'):
        super(ImprovAdminSite, self).__init__(name)
        if settings.DJANGO_ADMIN_SSO:
            self.login = gauth


ADMIN_SITE = ImprovAdminSite()

ADMIN_SITE.register(ArticleAdmin.model, ArticleAdmin)
ADMIN_SITE.register(BandAdmin.model, BandAdmin)
ADMIN_SITE.register(ContestantGroupAdmin.model, ContestantGroupAdmin)
ADMIN_SITE.register(FoulAdmin.model, FoulAdmin)
ADMIN_SITE.register(FoulTypeAdmin.model, FoulTypeAdmin)
ADMIN_SITE.register(GameAdmin.model, GameAdmin)
ADMIN_SITE.register(GameRulesAdmin.model, GameRulesAdmin)
ADMIN_SITE.register(ChapterAdmin.model, ChapterAdmin)
ADMIN_SITE.register(InspirationAdmin.model, InspirationAdmin)
ADMIN_SITE.register(LivePollVotingAdmin.model, LivePollVotingAdmin)
ADMIN_SITE.register(LocationAdmin.model, LocationAdmin)
ADMIN_SITE.register(MatchAdmin.model, MatchAdmin)
ADMIN_SITE.register(MatchStageAdmin.model, MatchStageAdmin)
ADMIN_SITE.register(PoemAdmin.model, PoemAdmin)
ADMIN_SITE.register(ProfileAdmin.model, ProfileAdmin)
ADMIN_SITE.register(ProfileGroupAdmin.model, ProfileGroupAdmin)
ADMIN_SITE.register(ReservationAdmin.model, ReservationAdmin)
ADMIN_SITE.register(ScorePointAdmin.model, ScorePointAdmin)
ADMIN_SITE.register(ScorePointPollAdmin.model, ScorePointPollAdmin)
ADMIN_SITE.register(ShowAdmin.model, ShowAdmin)
ADMIN_SITE.register(ShowParticipantAdmin.model, ShowParticipantAdmin)
ADMIN_SITE.register(ShowRoleAdmin.model, ShowRoleAdmin)
ADMIN_SITE.register(ShowTypeAdmin.model, ShowTypeAdmin)
ADMIN_SITE.register(ShowVolumeCalibrationAdmin.model, ShowVolumeCalibrationAdmin)
ADMIN_SITE.register(ShowVolumeCalibrationVotingAdmin.model, ShowVolumeCalibrationVotingAdmin)
ADMIN_SITE.register(UsualPlaceAdmin.model, UsualPlaceAdmin)
ADMIN_SITE.register(VolumeScrapeAdmin.model, VolumeScrapeAdmin)

ADMIN_SITE.register(auth_admin.Group, auth_admin.GroupAdmin)
ADMIN_SITE.register(auth_admin.User, auth_admin.UserAdmin)
ADMIN_SITE.register(Assignment, AssignmentAdmin)
