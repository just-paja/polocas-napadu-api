from django.db.models import ForeignKey, CASCADE

from photos.models import Photo


class LocationPhoto(Photo):
    profile = ForeignKey("Location", on_delete=CASCADE, related_name="photos",)
