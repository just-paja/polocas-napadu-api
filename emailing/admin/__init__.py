from django.utils.translation import ugettext_lazy as _

from fields.admin import ImprovAdminSite

from .notifications import EmailNotificationAdmin


class EmailingAdminSite(ImprovAdminSite):
    name = 'emailing'
    site_title = _('Emailing')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookup(EmailNotificationAdmin)


EMAILING_ADMIN = EmailingAdminSite()
