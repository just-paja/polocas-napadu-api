from django.db.models import BooleanField, CharField, Model
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin

class ProfileGroup(NameMixin):

    class Meta:
        verbose_name = _('Actor group')
        verbose_name_plural = _('Actor groups')

    public = BooleanField(default=False)
