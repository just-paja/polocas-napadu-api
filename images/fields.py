from django.db.models import ImageField as ThumbnailImageField
from django.utils.translation import ugettext_lazy as _


class ImageField(ThumbnailImageField):
    def __init__(self, *args, **kwargs):
        kwargs["blank"] = kwargs.get("blank", False)
        kwargs["null"] = kwargs.get("null", False)
        kwargs["verbose_name"] = _("Image")
        kwargs["help_text"] = _("imageHelpText")
        super().__init__(*args, **kwargs)
