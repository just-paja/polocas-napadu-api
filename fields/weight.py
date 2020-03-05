from django.db.models import Model, IntegerField
from django.utils.translation import ugettext_lazy as _


class WeightField(IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["blank"] = kwargs.get("blank", False)
        kwargs["null"] = kwargs.get("null", False)
        kwargs["default"] = kwargs.get("default", 100)
        kwargs["verbose_name"] = _("Weight")
        kwargs["help_text"] = _("weightHelpText")
        super().__init__(*args, **kwargs)


class WeightedMixin(Model):
    class Meta:
        abstract = True

    weight = WeightField()
    ordering = ('weight')
