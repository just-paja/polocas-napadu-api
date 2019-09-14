from graphene import Int, List, relay

from graphene_django.types import DjangoObjectType

from .models import Profile, ProfileGroup, ProfilePhoto


class ProfileGroupNode(DjangoObjectType):
    class Meta:
        model = ProfileGroup


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
    profile_list = List(ProfileNode, group=Int())
    profile_group_list = List(ProfileGroupNode)

    def resolve_profile_list(self, info, group=None):
        source = Profile.objects.get_visible()
        if group:
            source = source.filter(group=group)
        return source

    def resolve_profile_group_list(self, info):
        return ProfileGroup.objects.get_visible()
