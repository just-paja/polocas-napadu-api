from django.db.models import ForeignKey, CASCADE

from photos.models import Photo


class ShowTypePhoto(Photo):
    profile = ForeignKey("ShowType", on_delete=CASCADE, related_name="photos",)
