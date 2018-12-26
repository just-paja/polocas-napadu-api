from graphene import List

from graphene_django.types import DjangoObjectType

from .models import Location


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location


class Query:
    list_locations = List(LocationNode)

    def resolve_list_locations(self, info):
        return Location.objects.get_visible()
