from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django.db.models import BooleanField, URLField
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, VisibilityMixin, WeightedMixin
from images.fields import ImageField


class Sponsor(NameMixin, TimeStampedModel, VisibilityMixin, WeightedMixin):
    class Meta:
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    slug = AutoSlugField(_("Slug"), overwrite=True, populate_from="name")
    website = URLField(_("Website"), blank=True, null=True)
    logo = ImageField(
        upload_to="var/sponsors", verbose_name=_("Logo"),
    )
    on_site = BooleanField(
        default=False,
        help_text=_("Display this sponsor on site"),
        verbose_name=_("On site"),
    )
