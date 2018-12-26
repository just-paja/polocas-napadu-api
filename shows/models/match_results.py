from django_extensions.db.models import TimeStampedModel
from django.db.models import BooleanField, OneToOneField, PROTECT
from django.utils.translation import ugettext_lazy as _


class MatchResults(TimeStampedModel):

    class Meta:
        verbose_name = _('Match results')
        verbose_name_plural = _('Matches results')

    show = OneToOneField(
        'Show',
        on_delete=PROTECT,
        related_name='match_results',
    )
    closed = BooleanField(default=False)
