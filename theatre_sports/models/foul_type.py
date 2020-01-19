from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class FoulType(PublicResourceMixin):
    class Meta:
        verbose_name = _("FoulType")
        verbose_name_plural = _("Foul Types")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
