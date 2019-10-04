from django.db.models import ForeignKey, CASCADE

from photos.models import Photo

class ChapterPhoto(Photo):
    profile = ForeignKey(
        'Chapter',
        on_delete=CASCADE,
        related_name='photos',
    )
