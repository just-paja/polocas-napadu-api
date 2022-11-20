from graphene_django.types import DjangoObjectType

from .models import PriceLevel


class PriceLevelNode(DjangoObjectType):
    class Meta:
        model = PriceLevel
        fields = '__all__'
