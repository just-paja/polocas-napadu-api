from datetime import timedelta
from django.utils import timezone
from graphene import Boolean, Field, Int, List, ObjectType, String, Mutation
from graphene_django.types import DjangoObjectType

from .models import Workshop


class WorkshopNode(DjangoObjectType):
    class Meta:
        model = Workshop


class Query:
    workshop_list = List(
        WorkshopNode,
        future=Boolean(),
        limit=Int(),
        past=Boolean(),
        show_type_slug=String(),
        order_by=String(),
    )

    def resolve_workshop_list(self, info, **kwargs):
        future = kwargs.get("future") or False
        limit = kwargs.get("limit") or None
        past = kwargs.get("past") or False
        show_type_slug = kwargs.get("show_type_slug") or None
        order_by = kwargs.get("order_by") or "-start"
        source = Workshop.objects.get_visible().order_by(order_by)
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
