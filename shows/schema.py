import graphene

from graphene_django.types import DjangoObjectType

from . import models


class ShowType(DjangoObjectType):
    class Meta:
        model = models.Show


class ShowTypeType(DjangoObjectType):
    class Meta:
        model = models.ShowType


class ShowPhotoType(DjangoObjectType):
    class Meta:
        model = models.ShowPhoto


class Query:
    all_shows = graphene.List(ShowType)
    all_show_types = graphene.List(ShowTypeType)

    def resolve_all_shows(self, info, **kwargs):
        return models.Show.objects.all()

    def resolve_all_show_types(self, info, **kwargs):
        return models.ShowTypes.objects.all()
