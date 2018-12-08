from django.db.models import CharField, ForeignKey, Model, TextField, PROTECT
from django_extensions.db.models import TimeStampedModel


class Profile(TimeStampedModel):
    name = CharField(max_length=127)
    about = TextField()
    group = ForeignKey(
        'ProfileGroup',
        blank=True,
        null=True,
        on_delete=PROTECT,
    )
