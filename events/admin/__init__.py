from .event import EventAdmin, EventViewerAdmin
from .event_filter import EventFilter
from .event_participant import EventParticipantAdmin
from .participant_role import ParticipantRoleAdmin

MODELS = (EventAdmin, EventParticipantAdmin, ParticipantRoleAdmin,)
