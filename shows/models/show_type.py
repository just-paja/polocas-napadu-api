from django.db.models import Model, CharField, TextField


class ShowType(Model):
    name = CharField(max_length=50)
    description = TextField()
