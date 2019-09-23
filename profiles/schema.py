from graphene import Field, Int, List, String

from graphene_django.types import DjangoObjectType

from .models import Profile, ProfileGroup, ProfilePhoto


class ProfileGroupNode(DjangoObjectType):
    class Meta:
        model = ProfileGroup

def serialize_image_field(field, info):
    try:
        return info.context.build_absolute_uri(field.url)
    except ValueError:
        return None


class ProfilePhotoNode(DjangoObjectType):
    class Meta:
        model = ProfilePhoto

    def resolve_image(self, info, *_):
        return serialize_image_field(self.image, info)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile

    def resolve_avatar(self, info, *_):
        return serialize_image_field(self.avatar, info)


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
