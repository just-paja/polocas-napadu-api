from django.db.models import BooleanField, CharField, DateTimeField, ForeignKey, Model, PROTECT, TextField

class Event(Model):
    all_day = BooleanField()
    description = TextField()
    end = DateTimeField()
    name = CharField(max_length=50)
    start = DateTimeField()
    location = ForeignKey('locations.Location', on_delete=PROTECT)

    class Meta:
        abstract = True
