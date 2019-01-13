from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from fields import NameMixin, VisibilityMixin


class GameRules(NameMixin, VisibilityMixin, TimeStampedModel):

    class Meta:
        verbose_name = _('Game Rule')
        verbose_name_plural = _('Game Rules')

    description = TextField(max_length=255)
