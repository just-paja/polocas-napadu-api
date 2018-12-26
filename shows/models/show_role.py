from django_extensions.db.models import TimeStampedModel

from fields import NameMixin


class ShowRole(NameMixin, TimeStampedModel):
    pass
