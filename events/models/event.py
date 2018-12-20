from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django.db.models import BooleanField, CharField, DateTimeField, ForeignKey, PROTECT, TextField
from django.utils.translation import ugettext_lazy as _

class Event(TimeStampedModel):
    name = CharField(max_length=50)
    slug = AutoSlugField(_('Slug'), populate_from='name')
    start = DateTimeField()
    end = DateTimeField()
    all_day = BooleanField()
    location = ForeignKey('locations.Location', on_delete=PROTECT)
    description = TextField()

    class Meta:
        abstract = True
