from graphene import List, Int, ObjectType, String

from django.conf import settings
from django.urls import reverse


class ImageThumbnail(ObjectType):
    name = String()
    jpeg = String()
    webp = String()


class Image(ObjectType):
    height = Int()
    src = String()
    width = Int()
    thumbnails = List(ImageThumbnail)
    instance = None

    def __init__(self, instance):
        super().__init__()
        self.instance = instance

    def resolve_thumbnails(self, info):
        data = []
        for key in settings.THUMBNAILS.keys():
            thumb = ImageThumbnail()
            thumb.name = key
            thumb.jpeg = '%s?image=%s' % (
                info.context.build_absolute_uri(reverse(
                    'thumb',
                    kwargs={'image_format': 'jpeg', 'image_size': key}
                )),
                self.instance.name,
            )
            thumb.webp = '%s?image=%s' % (
                info.context.build_absolute_uri(reverse(
                    'thumb',
                    kwargs={'image_format': 'webp', 'image_size': key}
                )),
                self.instance.name,
            )
            data.append(thumb)
        return data


def serialize_image_field(field, info):
    img = Image(field)
    try:
        img.height = field.height
        img.width = field.width
        img.src = info.context.build_absolute_uri(field.url)
        return img
    except ValueError:
        return None
