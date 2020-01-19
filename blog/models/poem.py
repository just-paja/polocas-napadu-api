from django_extensions.db.models import AutoSlugField
from django.db.models import ForeignKey, IntegerField, PROTECT
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class Poem(PublicResourceMixin):
    class Meta:
        verbose_name = _("Poem")
        verbose_name_plural = _("Poems")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
    weight = IntegerField(
        default=0, help_text=_("weightHelpText"), verbose_name=_("Weight"),
    )
    author = ForeignKey("profiles.Profile", on_delete=PROTECT)
