from graphene import Field
from graphene_django.types import DjangoObjectType

from images.schema import Image


class PhotoNode(DjangoObjectType):
    image = Field(Image)

    class Meta:
        abstract = True

    def resolve_image(self, info, *_):
        img = Image(self.image)
        try:
            img.height = self.height
            img.width = self.width
            img.src = info.context.build_absolute_uri(self.image.url)
            return img
        except ValueError:
            return None
