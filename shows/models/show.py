from django.db.models import ForeignKey, PROTECT

from events.models import Event


class Show(Event):
    show_type = ForeignKey('showType', on_delete=PROTECT)
