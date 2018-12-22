import graphene

from graphene_django.types import DjangoObjectType

from .models import Location, LocationPhoto


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class LocationPhotoType(DjangoObjectType):
    class Meta:
        model = LocationPhoto


class Query:
    all_locations = graphene.List(LocationType)

    def resolve_all_locations(self, info, **kwargs):
        return Location.objects.get_visible()
