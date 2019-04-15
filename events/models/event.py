from django_extensions.db.fields import AutoSlugField
from django.db.models import (
    BooleanField,
    DateTimeField,
    ForeignKey,
    PROTECT,
)
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin, VisibilityManager


class EventManager(VisibilityManager):
    def get_recent(self):
        return self.get_visible().order('-start')


class Event(PublicResourceMixin):
    slug = AutoSlugField(_('Slug'), populate_from='name')
    start = DateTimeField()
    end = DateTimeField(null=True, blank=True)
    all_day = BooleanField(default=False)
    location = ForeignKey('locations.Location', on_delete=PROTECT)
    objects = EventManager()

    class Meta:
        abstract = True
