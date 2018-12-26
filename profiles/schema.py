from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import Profile


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile


class Query:
    get_profile = relay.Node.Field(ProfileNode)
    list_profiles = List(ProfileNode)

    def resolve_list_profiles(self, info):
        return Profile.objects.get_visible()
