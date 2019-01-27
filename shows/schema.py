from django.urls import reverse
from graphene import Int, List, Node, String

from graphene_django.types import DjangoObjectType

from .models import Show, ShowPhoto, ShowType, ShowTypePhoto



class ShowPhotoNode(DjangoObjectType):
    class Meta:
        model = ShowPhoto


class ShowNode(DjangoObjectType):
    inspiration_url = String()
    inspiration_qr_url = String()
    total_inspirations = Int()

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

    def resolve_total_inspirations(self, info):
        return self.inspirations.filter(discarded=False).count()


class ShowTypePhotoNode(DjangoObjectType):
    class Meta:
        model = ShowTypePhoto


class ShowTypeNode(DjangoObjectType):
    class Meta:
        model = ShowType


class Query:
    show = Node.Field(ShowNode)
    show_type = Node.Field(ShowTypeNode)
    show_list = List(ShowNode)
    show_type_list = List(ShowTypeNode)

    def resolve_show_list(self, info):
        return Show.objects.get_visible()

    def resolve_show_type_list(self, info):
        return ShowType.objects.get_visible()
