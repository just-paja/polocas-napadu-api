from django.db.models import Model, CharField


class NameField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 63
        kwargs['blank'] = False
        kwargs['null'] = False
        super().__init__(*args, **kwargs)


class NameMixin(Model):

    class Meta:
        abstract = True

    name = NameField()

    def __str__(self):
        return self.name
