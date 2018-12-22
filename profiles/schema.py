import graphene

from graphene_django.types import DjangoObjectType

from . import models


class ProfileType(DjangoObjectType):
    class Meta:
        model = models.Profile


class Query:
    all_profiles = graphene.List(ProfileType)

    def resolve_all_profiles(self, info, **kwargs):
        return models.Profile.objects.get_visible()
