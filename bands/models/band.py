from django.db.models import CharField, Model, URLField


class Band(Model):
    name = CharField(max_length=127)
    website = URLField(blank=True, null=True)
