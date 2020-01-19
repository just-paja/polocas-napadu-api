from django.db.models import ForeignKey, CASCADE

from photos.models import Photo


class ProfilePhoto(Photo):
    profile = ForeignKey("Profile", on_delete=CASCADE, related_name="photos",)
