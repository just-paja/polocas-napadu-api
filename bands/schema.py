from graphene import List, relay

from graphene_django.types import DjangoObjectType
from photos.schema import PhotoNode

from .models import Band, BandPhoto


class BandPhotoNode(PhotoNode):
    class Meta:
        model = BandPhoto
        fields = '__all__'


class BandNode(DjangoObjectType):
    class Meta:
        model = Band
        fields = '__all__'
        filter_fields = {
            "name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = [relay.Node]


class Query:
    get_band = relay.Node.Field(BandNode)
    list_bands = List(BandNode)

    def resolve_list_bands(self, info):
        return Band.objects.get_visible()
