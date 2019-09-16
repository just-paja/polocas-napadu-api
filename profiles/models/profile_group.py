from django.db.models import IntegerField
from django.utils.translation import ugettext_lazy as _

from fields import DescriptionMixin, NameMixin, VisibilityMixin


class ProfileGroup(NameMixin, DescriptionMixin, VisibilityMixin):

    class Meta:
        verbose_name = _('Actor group')
        verbose_name_plural = _('Actor groups')

    weight = IntegerField(
        default=0,
        help_text=_('weightHelpText'),
        verbose_name=_('Weight'),
    )
