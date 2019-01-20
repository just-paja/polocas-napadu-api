from django.urls import reverse
from graphene import List, Node, String

from graphene_django.types import DjangoObjectType

from .models import Show, ShowPhoto, ShowType, ShowTypePhoto



class ShowPhotoNode(DjangoObjectType):
    class Meta:
        model = ShowPhoto


class ShowNode(DjangoObjectType):
    inspiration_url = String()
    inspiration_qr_url = String()

    class Meta:
        model = Show

    def resolve_inspiration_url(self, info):
        return self.get_inspiration_url() # pylint: disable=E1101

    def resolve_inspiration_qr_url(self, info):
        return '%s://%s%s' % (
            'https' if info.context.is_secure() else 'http',
            info.context.get_host(),
            reverse('show_inspiration_qr', kwargs={
                'show_id': self.id, # pylint: disable=E1101
            })
        )


class ShowTypePhotoNode(DjangoObjectType):
    class Meta:
        model = ShowTypePhoto


class ShowTypeNode(DjangoObjectType):
    class Meta:
        model = ShowType


class Query:
    get_show = Node.Field(ShowNode)
    get_show_type = Node.Field(ShowTypeNode)
    list_shows = List(ShowNode)
    list_show_types = List(ShowTypeNode)

    def resolve_list_shows(self, info):
        return Show.objects.get_visible()

    def resolve_list_show_types(self, info):
        return ShowType.objects.get_visible()
