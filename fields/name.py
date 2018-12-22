from django.db.models import Model, CharField
from django.utils.translation import ugettext_lazy as _


class NameField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 63
        kwargs['blank'] = False
        kwargs['null'] = False
        kwargs['verbose_name'] = _('Name')
        kwargs['help_text'] = _('nameHelpText')
        super().__init__(*args, **kwargs)


class NameMixin(Model):

    class Meta:
        abstract = True

    name = NameField()

    def __str__(self):
        return self.name
