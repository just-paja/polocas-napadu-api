from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _

from fields import DescriptionMixin, NameMixin, VisibilityMixin


class ProfileGroup(NameMixin, DescriptionMixin, VisibilityMixin):

    class Meta:
        verbose_name = _('Actor group')
        verbose_name_plural = _('Actor groups')
