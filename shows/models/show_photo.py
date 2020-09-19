from django.db.models import ForeignKey, CASCADE

from photos.models import Photo


class ShowPhoto(Photo):
    show = ForeignKey("shows.Show", on_delete=CASCADE, related_name="photos",)
