from django.urls import reverse
from graphql import GraphQLError
from graphene import Boolean, Field, Int, List, Node, ObjectType, String, Mutation

from graphene_django.types import DjangoObjectType

from fields import append_host_from_context
from inspirations.models import Inspiration

from .models import Show, ShowParticipant, ShowPhoto, ShowType, ShowTypePhoto


class ShowParticipantNode(DjangoObjectType):
    class Meta:
        model = ShowParticipant


class ShowPhotoNode(DjangoObjectType):
    class Meta:
        model = ShowPhoto


class ShowNode(DjangoObjectType):
    inspiration_qr_url = String()
    total_inspirations = Int()

    class Meta:
        model = Show

    def resolve_inspiration_qr_url(self, info):
        path = reverse('show_inspiration_qr', kwargs={
            'show_id': self.id,
        })
        return append_host_from_context(path, info.context)

    def resolve_total_inspirations(self, info):
        return self.inspirations.filter(discarded=False).count()


class ShowTypePhotoNode(DjangoObjectType):
    class Meta:
        model = ShowTypePhoto


class ShowTypeNode(DjangoObjectType):
    class Meta:
        model = ShowType


class AddInspiration(Mutation):
    class Arguments:
        show_id = Int(required=True)
        inspiration_text = String(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, show_id, inspiration_text):
        show = Show.objects.get(pk=show_id)
        exists = show.inspirations.filter(text=inspiration_text).count() > 0
        if exists:
            return GraphQLError('already-exists')
        Inspiration.objects.create(
            show=show,
            text=inspiration_text,
        )
        return AddInspiration(ok=True)


class Query:
    show = Field(ShowNode, id=Int())
    show_type = Node.Field(ShowTypeNode)
    show_list = List(ShowNode)
    show_type_list = List(ShowTypeNode)

    def resolve_show(self, info, id):
        return Show.objects.get_visible().get(pk=id)

    def resolve_show_list(self, info):
        return Show.objects.get_visible()

    def resolve_show_type_list(self, info):
        return ShowType.objects.get_visible()


class Mutations(ObjectType):
    add_inspiration = AddInspiration.Field()
