from django.db.models import CharField, URLField
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class Location(PublicResourceMixin):
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    address = CharField(max_length=255)
    gps = CharField(max_length=127, blank=True, null=True)
    website = URLField(blank=True, null=True)
