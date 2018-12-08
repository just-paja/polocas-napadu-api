from django.db.models import CharField, Model, TextField, URLField


class Location(Model):
    address = CharField(max_length=255)
    description = TextField()
    gps = CharField(max_length=127, blank=True, null=True)
    name = CharField(max_length=127)
    website = URLField(blank=True, null=True)
