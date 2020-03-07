from .config import ConfigurationAdminSite
from .content import ContentAdminSite
from .emailing import EmailingAdminSite

CONFIGURATION_ADMIN = ConfigurationAdminSite()
CONTENT_ADMIN = ContentAdminSite()
EMAILING_ADMIN = EmailingAdminSite()
