from django.db.models import Manager, Model, PositiveIntegerField
from django.utils.translation import gettext_lazy as _


VISIBILITY_PRIVATE = 1
VISIBILITY_PUBLIC = 2
VISIBILITY_DELETED = 3

VISIBILITY_CHOICES = (
    (VISIBILITY_PRIVATE, _("Private")),
    (VISIBILITY_PUBLIC, _("Public")),
    (VISIBILITY_DELETED, _("Deleted")),
)


class VisibilityField(PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = VISIBILITY_CHOICES
        kwargs["default"] = VISIBILITY_PUBLIC
        kwargs["verbose_name"] = _("Visibility")
        kwargs["help_text"] = _("visibilityHelpText")
        super().__init__(*args, **kwargs)


class VisibilityManager(Manager):
    def get_visible(self):
        return self.filter(visibility=VISIBILITY_PUBLIC)


class VisibilityMixin(Model):
    class Meta:
        abstract = True

    objects = VisibilityManager()
    visibility = VisibilityField()
