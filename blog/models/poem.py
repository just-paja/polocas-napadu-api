from django_extensions.db.models import AutoSlugField
from django.db.models import ForeignKey, PROTECT
from django.utils.translation import gettext_lazy as _

from fields import PublicResourceMixin, WeightedMixin


class Poem(PublicResourceMixin, WeightedMixin):
    class Meta:
        verbose_name = _("Poem")
        verbose_name_plural = _("Poems")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
    author = ForeignKey("profiles.Profile", on_delete=PROTECT)
