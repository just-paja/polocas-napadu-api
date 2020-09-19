from graphene import List
from graphene_django.types import DjangoObjectType

from .models import Workshop


class WorkshopNode(DjangoObjectType):
    class Meta:
        model = Workshop


class Query:
    workshop_list = List(WorkshopNode)

    def resolve_workshop_list(self, info):
        return Workshop.objects.get_visible()
