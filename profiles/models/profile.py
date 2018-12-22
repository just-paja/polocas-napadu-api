from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, ForeignKey, Model, TextField, PROTECT
from django.utils.translation import ugettext_lazy as _

from fields import VisibilityManager, VisibilityMixin


class ProfileManager(VisibilityManager):
    pass


class Profile(TimeStampedModel, VisibilityMixin):
    name = CharField(max_length=127)
    slug = AutoSlugField(_('Slug'), populate_from='name')
    about = TextField()
    group = ForeignKey(
        'ProfileGroup',
        blank=True,
        null=True,
        on_delete=PROTECT,
    )
    objects = ProfileManager()
