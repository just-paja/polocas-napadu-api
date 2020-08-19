from graphene import Field, Int, List, String

from graphene_django.types import DjangoObjectType
from photos.schema import Image, PhotoNode, serialize_image_field

from .models import Profile, ProfileGroup, ProfilePhoto, Sponsor


class ProfileGroupNode(DjangoObjectType):
    class Meta:
        model = ProfileGroup


class ProfilePhotoNode(PhotoNode):
    class Meta:
        model = ProfilePhoto


class ProfileNode(DjangoObjectType):
    avatar = Field(Image)

    class Meta:
        model = Profile

    def resolve_avatar(self, info, *_):
        return serialize_image_field(self.avatar, info)


class SponsorNode(DjangoObjectType):
    logo = Field(Image)

    class Meta:
        model = Sponsor

    def resolve_logo(self, info, *_):
        return serialize_image_field(self.logo, info)


class Query:
    profile = Field(ProfileNode, slug=String())
    profile_list = List(ProfileNode, group=Int())
    profile_group_list = List(ProfileGroupNode)
    site_sponsor_list = List(SponsorNode)

    def resolve_profile(self, info, slug):
        return Profile.objects.get_visible().filter(slug=slug).first()

    def resolve_profile_list(self, info, group=None):
        source = Profile.objects.get_visible()
        if group:
            source = source.filter(group=group)
        return source

    def resolve_profile_group_list(self, info):
        return ProfileGroup.objects.get_visible().order_by("weight")

    def resolve_site_sponsor_list(self, info):
        return Sponsor.objects.filter(on_site=True).order_by("weight")
