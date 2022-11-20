from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone
from graphene import Boolean, Field, Int, List, ObjectType, String, Mutation
from graphql import GraphQLError

from graphene_django.types import DjangoObjectType

from events.schema import EventNode
from fields import append_host_from_context
from inspirations.models import Inspiration
from photos.schema import PhotoNode

from .models import (
    Show,
    ShowPhoto,
    ShowType,
    ShowTypePhoto,
)


class ShowPhotoNode(PhotoNode):
    class Meta:
        model = ShowPhoto
        fields = '__all__'


class ShowNode(EventNode):
    inspiration_qr_url = String()
    total_inspirations = Int()

    class Meta:
        model = Show
        fields = '__all__'

    def resolve_inspiration_qr_url(self, info):
        path = reverse("show_inspiration_qr", kwargs={"show_id": self.id, })
        return append_host_from_context(path, info.context)

    def resolve_total_inspirations(self, info):
        return self.inspirations.filter(discarded=False).count()


class ShowTypePhotoNode(PhotoNode):
    class Meta:
        model = ShowTypePhoto
        fields = '__all__'


class ShowTypeNode(DjangoObjectType):
    class Meta:
        model = ShowType
        fields = '__all__'

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


def filter_limits(source, **kwargs):
    future = kwargs.get("future") or False
    limit = kwargs.get("limit") or None
    past = kwargs.get("past") or False
    yesterday = timezone.now() - timedelta(days=1)
    if future:
        source = source.filter(start__gte=yesterday)
    if past:
        source = source.filter(start__lt=yesterday)
    if limit:
        source = source[:limit]
    return source


def filter_inspirations(source, use_inspirations=None):
    if use_inspirations is not None:
        return source.filter(use_inspirations=use_inspirations)
    return source


class Query:
    show = Field(ShowNode, show_id=Int(), slug=String(), use_inspirations=Boolean())
    show_photo_list = List(ShowPhotoNode, limit=Int())
    show_type = Field(ShowTypeNode, slug=String())
    show_type_list = List(ShowTypeNode)
    show_list = List(
        ShowNode,
        future=Boolean(),
        limit=Int(),
        month=String(),
        past=Boolean(),
        show_type_slug=String(),
        order_by=String(),
        use_inspirations=Boolean(),
    )

    def resolve_show(self, info, show_id=None, slug=None, use_inspirations=None):
        try:
            query = Show.objects.get_visible()
            if slug:
                query = query.filter(slug=slug)
            else:
                query = query.filter(pk=show_id)
            return filter_inspirations(query, use_inspirations).get()
        except Show.DoesNotExist:
            return None

    def resolve_show_list(self, info, **kwargs):
        month = kwargs.get("month") or None
        show_type_slug = kwargs.get("show_type_slug") or None
        order_by = kwargs.get("order_by") or "-start"
        use_inspirations = kwargs.get('use_inspirations', None)
        source = Show.objects.get_visible().order_by(order_by)
        source = filter_inspirations(source, use_inspirations)
        if show_type_slug:
            try:
                show_type = ShowType.objects.get(slug=show_type_slug)
            except ShowType.DoesNotExist:
                return []
            source = source.filter(show_type=show_type)
        if month:
            try:
                date_year, date_month = month.split('-')
                month_start = datetime(year=int(date_year), month=int(date_month), day=1)
                next_month_start = month_start + relativedelta(months=1)
            except ValueError:
                return []
            source = source.exclude(
                Q(end__lt=month_start) |
                Q(start__lt=month_start, end__isnull=True) |
                Q(start__gte=next_month_start),
            )
        else:
            return filter_limits(source, **kwargs)
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

    def resolve_show_photo_list(self, info, **kwargs):
        limit = kwargs.get("limit") or None
        source = ShowPhoto.objects.get_visible().order_by('-created')
        if limit:
            source = source[:10]
        return source


class Mutations(ObjectType):
    add_inspiration = AddInspiration.Field()
