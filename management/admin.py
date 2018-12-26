from django.contrib.admin import AdminSite
from django.contrib.auth import admin as auth_admin

from bands.models import Band
from locations.models import Location
from profiles.models import Profile, ProfileGroup
from shows.models import MatchResults, Show, ShowRole, ShowType

from .models import (
    BandAdmin,
    LocationAdmin,
    MatchResultsAdmin,
    ProfileAdmin,
    ProfileGroupAdmin,
    ShowAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
)


class ImprovAdminSite(AdminSite):
    site_header = 'Poločas nápadu'


ADMIN_SITE = ImprovAdminSite()

ADMIN_SITE.register(Band, BandAdmin)
ADMIN_SITE.register(Location, LocationAdmin)
ADMIN_SITE.register(MatchResults, MatchResultsAdmin)
ADMIN_SITE.register(Profile, ProfileAdmin)
ADMIN_SITE.register(ProfileGroup, ProfileGroupAdmin)
ADMIN_SITE.register(Show, ShowAdmin)
ADMIN_SITE.register(ShowRole, ShowRoleAdmin)
ADMIN_SITE.register(ShowType, ShowTypeAdmin)

ADMIN_SITE.register(auth_admin.Group, auth_admin.GroupAdmin)
ADMIN_SITE.register(auth_admin.User, auth_admin.UserAdmin)
