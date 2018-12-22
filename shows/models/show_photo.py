from django.db.models import ForeignKey, CASCADE

from photos.models import Photo


class ShowPhoto(Photo):
    profile = ForeignKey(
        'Show',
        on_delete=CASCADE,
        related_name='photos',
    )
