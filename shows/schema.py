from datetime import timedelta
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from graphene import Boolean, Field, Int, List, ObjectType, String, Mutation
from graphql import GraphQLError

from graphene_django.types import DjangoObjectType

from fields import append_host_from_context
from inspirations.models import Inspiration

from .models import Show, ShowParticipant, ShowPhoto, ShowRole, ShowType, ShowTypePhoto


class ShowRoleNode(DjangoObjectType):
    class Meta:
        model = ShowRole


class ShowParticipantNode(DjangoObjectType):
    class Meta:
        model = ShowParticipant


class ShowPhotoNode(DjangoObjectType):
    class Meta:
        model = ShowPhoto


class ShowNode(DjangoObjectType):
    inspiration_qr_url = String()
    total_inspirations = Int()
    showsParticipants = List(ShowParticipantNode)

    class Meta:
        model = Show

    def resolve_inspiration_qr_url(self, info):
        path = reverse("show_inspiration_qr", kwargs={"show_id": self.id, })
        return append_host_from_context(path, info.context)

    def resolve_total_inspirations(self, info):
        return self.inspirations.filter(discarded=False).count()

    def resolve_showsParticipants(self, info):
        return self.showsParticipants.order_by('role__weight')


class ShowTypePhotoNode(DjangoObjectType):
    class Meta:
        model = ShowTypePhoto


class ShowTypeNode(DjangoObjectType):
    class Meta:
        model = ShowType

    show_count = Int()

    def resolve_show_count(self, *_):
        now = timezone.now()
        return self.shows.get_visible().filter(start__lt=now).count()


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
            return GraphQLError("already-exists")
        Inspiration.objects.create(
            show=show, text=inspiration_text,
        )
        return AddInspiration(ok=True)


class Query:
    show = Field(ShowNode, show_id=Int(), slug=String())
    show_type = Field(ShowTypeNode, slug=String())
    show_type_list = List(ShowTypeNode)
    show_list = List(
        ShowNode,
        future=Boolean(),
        limit=Int(),
        past=Boolean(),
        show_type_slug=String(),
        order_by=String(),
    )

    def resolve_show(self, info, show_id=None, slug=None):
        try:
            if slug:
                return Show.objects.get_visible().get(slug=slug)
            return Show.objects.get_visible().get(pk=show_id)
        except Show.DoesNotExist:
            return None

    def resolve_show_list(self, info, **kwargs):
        future = kwargs.get("future") or False
        limit = kwargs.get("limit") or None
        past = kwargs.get("past") or False
        show_type_slug = kwargs.get("show_type_slug") or None
        order_by = kwargs.get("order_by") or "-start"
        source = Show.objects.get_visible().order_by(order_by)
        yesterday = timezone.now() - timedelta(days=1)
        if show_type_slug:
            try:
                show_type = ShowType.objects.get(slug=show_type_slug)
            except ShowType.DoesNotExist:
                return []
            source = source.filter(show_type=show_type)
        if future:
            source = source.filter(start__gte=yesterday)
        if past:
            source = source.filter(start__lt=yesterday)
        if limit:
            source = source[:limit]
        return source

    def resolve_show_type(self, info, slug=None):
        try:
            return ShowType.objects.get_visible().get(slug=slug)
        except ShowType.DoesNotExist:
            return None

    def resolve_show_type_list(self, info):
        return (
            ShowType.objects.get_visible()
            .annotate(count=Count("shows__id"),)
            .order_by("-count")
        )


class Mutations(ObjectType):
    add_inspiration = AddInspiration.Field()
