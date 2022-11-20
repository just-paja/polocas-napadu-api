from django.db.models import ForeignKey, PositiveIntegerField, PROTECT
from django.utils.translation import gettext_lazy as _

from fields import PublicResourceMixin

PLACE_USUAL_STAGE = 1

PLACE_TYPES = [(PLACE_USUAL_STAGE, _("usualStage"))]


class UsualPlace(PublicResourceMixin):
    class Meta:
        verbose_name = _("Usual Place")
        verbose_name_plural = _("Usual Places")

    location = ForeignKey("Location", on_delete=PROTECT, verbose_name=_("Location"),)

    place_type = PositiveIntegerField(
        blank=True, choices=PLACE_TYPES, null=True, verbose_name=_("Place type")
    )

    def get_location_name(self):
        return self.location.name


UsualPlace.get_location_name.short_description = _("Location")
