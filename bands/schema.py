import graphene

from graphene_django.types import DjangoObjectType

from .models import Band, BandPhoto

class BandType(DjangoObjectType):
    class Meta:
        model = Band

class BandPhotoType(DjangoObjectType):
    class Meta:
        model = BandPhoto

class Query:
    all_bands = graphene.List(BandType)

    def resolve_all_bands(self, info, **kwargs):
        return Band.objects.all()
