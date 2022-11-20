from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

from fields import PublicResourceMixin


class GameRules(PublicResourceMixin):
    class Meta:
        verbose_name = _("Game Rule")
        verbose_name_plural = _("Game Rules")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
