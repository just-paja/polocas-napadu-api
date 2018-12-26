from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import Band, BandPhoto


class BandPhotoNode(DjangoObjectType):
    class Meta:
        model = BandPhoto


class BandNode(DjangoObjectType):
    class Meta:
        model = Band
        filter_fields = {
            'name': ['iexact', 'icontains', 'istartswith'],
        }
        interfaces = [relay.Node]


class Query:
    get_band = relay.Node.Field(BandNode)
    list_bands = List(BandNode)

    def resolve_list_bands(self, info):
        return Band.objects.get_visible()
