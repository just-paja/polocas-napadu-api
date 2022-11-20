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
        fields = '__all__'


class EventTicketPriceNode(DjangoObjectType):
    class Meta:
        model = EventTicketPrice
        fields = '__all__'


class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        fields = '__all__'

    ticket_prices = List(EventTicketPriceNode)
    participants = List(EventParticipantNode)

    def resolve_ticket_prices(self, info):
        return self.ticket_prices.all()

    def resolve_participants(self, info): # noqa
        return self.eventParticipants.order_by('role__weight')


class ParticipantRoleNode(DjangoObjectType):
    class Meta:
        model = ParticipantRole
        fields = '__all__'


class Query:
    participant_role_list = List(ParticipantRoleNode)
