from graphene import Field, Int, ObjectType, String
from graphene_django.types import DjangoObjectType


class Image(ObjectType):
    height = Int()
    src = String()
    width = Int()


def serialize_image_field(field, info):
    img = Image()
    try:
        img.height = field.height
        img.width = field.width
        img.src = info.context.build_absolute_uri(field.url)
        return img
    except ValueError:
        return None


class PhotoNode(DjangoObjectType):
    image = Field(Image)

    class Meta:
        abstract = True

    def resolve_image(self, info, *_):
        return serialize_image_field(self.image, info)
