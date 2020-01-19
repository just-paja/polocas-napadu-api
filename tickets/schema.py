from graphene import Field, Int, String
from graphene_django.types import DjangoObjectType
from django.db.models import Sum

from shows.models import Show

from .models import Reservation, STATUS_CONFIRMED


class ReservationNode(DjangoObjectType):
    class Meta:
        model = Reservation


class Query:
    reservation_count = Field(Int, show_slug=String())

    def resolve_reservation_count(self, info, show_slug):
        try:
            show = Show.objects.get(slug=show_slug)
        except Show.DoesNotExist:
            return 0
        obj = Reservation.objects.filter(show=show, status=STATUS_CONFIRMED,).aggregate(
            Sum("seat_count")
        )
        return obj["seat_count__sum"] or 0
