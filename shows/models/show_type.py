from django_extensions.db.fields import AutoSlugField
from django.db.models import BooleanField, TextField
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class ShowType(PublicResourceMixin):
    class Meta:
        verbose_name = _("Show type")
        verbose_name_plural = _("Show types")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
    short_description = TextField(
        verbose_name=_("Short Description"), blank=False, null=False,
    )
    use_games = BooleanField(
        blank=False, default=False, null=False, verbose_name=_("Use games"),
    )
    use_fouls = BooleanField(
        blank=False, default=False, null=False, verbose_name=_("Use fouls"),
    )
