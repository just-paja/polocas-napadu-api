from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField

from fields import NameMixin


class ShowRole(NameMixin, TimeStampedModel):
    pass
