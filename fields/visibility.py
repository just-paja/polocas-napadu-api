from django.db.models import Manager, Model, PositiveIntegerField

VISIBILITY_PRIVATE = 1
VISIBILITY_PUBLIC = 2
VISIBILITY_DELETED = 3

VISIBILITY_CHOICES = (
    (VISIBILITY_PRIVATE, 'Private'),
    (VISIBILITY_PUBLIC, 'Public'),
    (VISIBILITY_DELETED, 'Deleted'),
)

class VisibilityField(PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = VISIBILITY_CHOICES
        kwargs['default'] = VISIBILITY_PUBLIC
        super().__init__(*args, **kwargs)


class VisibilityManager(Manager):

    def get_visible(self):
        return self.filter(visibility=VISIBILITY_PUBLIC)


class VisibilityMixin(Model):
    class Meta:
        abstract = True

    objects = VisibilityManager()
    visibility = VisibilityField()
