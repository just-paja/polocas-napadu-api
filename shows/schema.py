from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from graphene import Boolean, Field, Int, List, Node, ObjectType, String, Mutation
from graphql import GraphQLError

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
    show = Field(ShowNode, show_id=Int(), slug=String())
    show_type = Node.Field(ShowTypeNode)
    show_type_list = List(ShowTypeNode)
    show_list = List(
        ShowNode,
        future=Boolean(),
        limit=Int(),
        past=Boolean()
    )

    def resolve_show(self, info, show_id=None, slug=None):
        try:
            if slug:
                return Show.objects.get_visible().get(slug=slug)
            return Show.objects.get_visible().get(pk=show_id)
        except Show.DoesNotExist:
            return None

    def resolve_show_list(self, info, future=False, past=False, limit=None):
        source = Show.objects.get_visible()
        yesterday = timezone.now() - timedelta(days=1)
        if future:
            source = source.filter(start__gte=yesterday)
        if past:
            source = source.filter(start__lt=yesterday)
        if limit:
            source = source[:limit]
        return source

    def resolve_show_type_list(self, info):
        return ShowType.objects.get_visible()


class Mutations(ObjectType):
    add_inspiration = AddInspiration.Field()
