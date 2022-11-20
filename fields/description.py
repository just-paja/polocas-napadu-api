from django.db.models import Model, TextField
from django.utils.translation import gettext_lazy as _


class DescriptionField(TextField):
    def __init__(self, *args, **kwargs):
        kwargs["blank"] = kwargs.get("blank", False)
        kwargs["null"] = kwargs.get("null", False)
        kwargs["verbose_name"] = _("Description")
        kwargs["help_text"] = _("nameDescriptionText")
        super().__init__(*args, **kwargs)


class DescriptionMixin(Model):
    class Meta:
        abstract = True

    description = DescriptionField()
