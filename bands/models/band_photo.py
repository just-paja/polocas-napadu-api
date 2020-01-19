from django.db.models import ForeignKey, CASCADE

from photos.models import Photo


class BandPhoto(Photo):
    profile = ForeignKey("Band", on_delete=CASCADE, related_name="photos",)
