from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import Profile, ProfilePhoto


class ProfilePhotoNode(DjangoObjectType):
    class Meta:
        model = ProfilePhoto


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile

    avatar = relay.Node.Field(ProfilePhotoNode)

    def resolve_avatar(self, info):
        return self.get_avatar()


class Query:
    profile = relay.Node.Field(ProfileNode)
    profile_list = List(ProfileNode)

    def resolve_profile_list(self, info):
        return Profile.objects.get_visible()
