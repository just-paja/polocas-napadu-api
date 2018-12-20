from django.contrib.admin import AdminSite
from django.contrib.auth import admin as auth_admin

from bands.models import Band
from locations.models import Location
from profiles.models import Profile
from shows.models import MatchResults, Show, ShowRole, ShowType


from .models import (
    BandAdmin,
    LocationAdmin,
    MatchResultsAdmin,
    ProfileAdmin,
    ShowAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
)

admin = AdminSite()

admin.register(Band, BandAdmin)
admin.register(Location, LocationAdmin)
admin.register(MatchResults, MatchResultsAdmin)
admin.register(Profile, ProfileAdmin)
admin.register(Show, ShowAdmin)
admin.register(ShowRole, ShowRoleAdmin)
admin.register(ShowType, ShowTypeAdmin)

admin.register(auth_admin.Group, auth_admin.GroupAdmin)
admin.register(auth_admin.User, auth_admin.UserAdmin)
