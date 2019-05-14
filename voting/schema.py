from graphene_django.types import DjangoObjectType

from .models import VolumeScrape

class VolumeScrapeNode(DjangoObjectType):
    class Meta:
        model = VolumeScrape
