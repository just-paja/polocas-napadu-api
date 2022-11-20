from django.utils.translation import gettext_lazy as _

from fields import DescriptionMixin, NameMixin, VisibilityMixin, WeightedMixin


class ProfileGroup(NameMixin, DescriptionMixin, VisibilityMixin, WeightedMixin):
    class Meta:
        verbose_name = _("Actor group")
        verbose_name_plural = _("Actor groups")
