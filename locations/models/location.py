from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, TextField, URLField
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, VisibilityMixin


class Location(NameMixin, TimeStampedModel, VisibilityMixin):

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    description = TextField()
    address = CharField(max_length=255)
    gps = CharField(max_length=127, blank=True, null=True)
    website = URLField(blank=True, null=True)
