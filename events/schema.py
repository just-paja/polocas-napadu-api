from graphene import List
from graphene_django.types import DjangoObjectType

from .models import (
    Event,
    EventParticipant,
    EventTicketPrice,
    ParticipantRole
)


class EventParticipantNode(DjangoObjectType):
    class Meta:
        model = EventParticipant


class EventTicketPriceNode(DjangoObjectType):
    class Meta:
        model = EventTicketPrice


class EventNode(DjangoObjectType):
    class Meta:
        model = Event

    ticket_prices = List(EventTicketPriceNode)
    participants = List(EventParticipantNode)

    def resolve_ticket_prices(self, info):
        return self.ticket_prices.all()

    def resolve_participants(self, info): # noqa
        return self.eventParticipants.order_by('role__weight')


class ParticipantRoleNode(DjangoObjectType):
    class Meta:
        model = ParticipantRole


class Query:
    participant_role_list = List(ParticipantRoleNode)
