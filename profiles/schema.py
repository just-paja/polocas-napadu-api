from graphene import Field, Int, List, String, relay

from graphene_django.types import DjangoObjectType

from .models import Profile, ProfileGroup, ProfilePhoto


class ProfileGroupNode(DjangoObjectType):
    class Meta:
        model = ProfileGroup


class ProfilePhotoNode(DjangoObjectType):
    class Meta:
        model = ProfilePhoto

    def resolve_image(self, *_):
        return self.image.url


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile

    avatar = relay.Node.Field(ProfilePhotoNode)

    def resolve_avatar(self, info):
        return self.get_avatar()


class Query:
    profile = Field(ProfileNode, slug=String())
    profile_list = List(ProfileNode, group=Int())
    profile_group_list = List(ProfileGroupNode)

    def resolve_profile(self, info, slug):
        return Profile.objects.get_visible().filter(slug=slug).first()

    def resolve_profile_list(self, info, group=None):
        source = Profile.objects.get_visible()
        if group:
            source = source.filter(group=group)
        return source

    def resolve_profile_group_list(self, info):
        return ProfileGroup.objects.get_visible().order_by('weight')
