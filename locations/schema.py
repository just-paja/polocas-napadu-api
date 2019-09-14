from graphene import Int, List

from graphene_django.types import DjangoObjectType

from .models import Location, UsualPlace


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location


class UsualPlaceNode(DjangoObjectType):
    class Meta:
        model = UsualPlace


class Query:
    location_list = List(LocationNode)
    usual_place_list = List(UsualPlaceNode, place_type=Int())

    def resolve_location_list(self, info):
        return Location.objects.get_visible()

    def resolve_usual_place_list(self, info, place_type=None):
        source = UsualPlace.objects.get_visible()
        if place_type:
            source = source.filter(place_type=place_type)
        return source
