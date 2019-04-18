from django.db.models import ForeignKey, PROTECT
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class UsualPlace(PublicResourceMixin):
    class Meta:
        verbose_name = _('Usual Place')
        verbose_name_plural = _('Usual Places')

    location = ForeignKey(
        'Location',
        on_delete=PROTECT,
        verbose_name=_('Location'),
    )

    def get_location_name(self):
        return self.location.name

UsualPlace.get_location_name.short_description = _('Location')
