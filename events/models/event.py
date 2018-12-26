from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django.db.models import (
    BooleanField,
    DateTimeField,
    ForeignKey,
    PROTECT,
    TextField,
)
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, VisibilityManager, VisibilityMixin


class EventManager(VisibilityManager):
    def get_recent(self):
        return self.get_visible().order('-start')


class Event(TimeStampedModel, NameMixin, VisibilityMixin):
    slug = AutoSlugField(_('Slug'), populate_from='name')
    start = DateTimeField()
    end = DateTimeField(null=True, blank=True)
    all_day = BooleanField(default=False)
    location = ForeignKey('locations.Location', on_delete=PROTECT)
    description = TextField()
    objects = EventManager()

    class Meta:
        abstract = True
