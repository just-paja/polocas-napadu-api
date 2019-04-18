from graphene import List

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
    usual_place_list = List(UsualPlaceNode)

    def resolve_location_list(self, info):
        return Location.objects.get_visible()

    def resolve_usual_place_list(self, info):
        return UsualPlace.objects.get_visible()
