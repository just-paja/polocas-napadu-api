from django.db.models import CharField, URLField
from django.utils.translation import gettext_lazy as _

from fields import PublicResourceMixin


class Location(PublicResourceMixin):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    address = CharField(max_length=255, verbose_name=_("Address"))
    city = CharField(blank=True, max_length=127, null=True, verbose_name=_("City"),)
    gps = CharField(
        blank=True, max_length=127, null=True, verbose_name=_("GPS coordinates"),
    )
    website = URLField(blank=True, null=True, verbose_name=_("Website"))
