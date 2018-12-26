from django_extensions.db.models import TimeStampedModel
from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, VisibilityMixin


class ShowType(NameMixin, TimeStampedModel, VisibilityMixin):

    class Meta:
        verbose_name = _('Show type')
        verbose_name_plural = _('Show types')

    description = TextField()
