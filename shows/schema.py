from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import Show, ShowPhoto, ShowType, ShowTypePhoto



class ShowPhotoNode(DjangoObjectType):
    class Meta:
        model = ShowPhoto


class ShowNode(DjangoObjectType):
    class Meta:
        model = Show


class ShowTypePhotoNode(DjangoObjectType):
    class Meta:
        model = ShowTypePhoto


class ShowTypeNode(DjangoObjectType):
    class Meta:
        model = ShowType


class Query:
    get_show = relay.Node.Field(ShowNode)
    get_show_type = relay.Node.Field(ShowTypeNode)
    list_shows = List(ShowNode)
    list_show_types = List(ShowTypeNode)

    def resolve_list_shows(self, info):
        return Show.objects.get_visible()

    def resolve_list_show_types(self, info):
        return ShowType.objects.get_visible()
