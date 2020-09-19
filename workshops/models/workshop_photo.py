from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _

from photos.models import Photo


class WorkshopPhoto(Photo):
    workshop = ForeignKey(
        "Workshop",
        on_delete=CASCADE,
        related_name="photos",
        verbose_name=_("Photos"),
    )
