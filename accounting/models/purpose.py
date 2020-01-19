from django.db.models import ManyToManyField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from fields import DescriptionMixin, NameMixin


class Purpose(
    TimeStampedModel,
    NameMixin,
    DescriptionMixin,
):
    def get_promise_count(self):
        return self.promises.count()


class PurposeCategory(
    TimeStampedModel,
    NameMixin,
    DescriptionMixin,
):
    class Meta:
        verbose_name = _('purpose category')
        verbose_name_plural = _('purpose categories')

    purposes = ManyToManyField(
        'Purpose',
        blank=True,
        related_name='categories',
    )
