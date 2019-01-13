from graphene import List, relay

from graphene_django.types import DjangoObjectType

from .models import Inspiration


class InspirationNode(DjangoObjectType):
    class Meta:
        model = Inspiration


class Query:
    get_inspiration = relay.Node.Field(InspirationNode)
    list_inspiration = List(InspirationNode)

    def resolve_list_inspirations(self, info):
        return Inspiration.objects.all()
