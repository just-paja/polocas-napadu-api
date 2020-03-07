from django.utils.translation import ugettext_lazy as _

from notifications.admin import EmailNotificationAdmin
from fields.admin import ImprovAdminSite


class EmailingAdminSite(ImprovAdminSite):
    name = 'emailing'
    site_title = _('Emailing')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookup(EmailNotificationAdmin)
