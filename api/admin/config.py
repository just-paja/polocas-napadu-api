from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from fields.admin import ImprovAdminSite


class ConfigurationAdminSite(ImprovAdminSite):
    name = 'configuration'
    site_title = _('Configuration')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(auth_admin.Group, auth_admin.GroupAdmin)
        self.register(auth_admin.User, auth_admin.UserAdmin)
