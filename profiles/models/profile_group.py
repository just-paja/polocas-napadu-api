from django.db.models import BooleanField, CharField, Model


class ProfileGroup(Model):
    name = CharField(max_length=63)
    public = BooleanField(default=False)
