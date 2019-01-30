"""Import all models."""

from .bands import BandAdmin, BandPhotoAdmin
from .games import GameAdmin, GameRulesAdmin
from .inspirations import InspirationAdmin
from .locations import LocationAdmin, LocationPhotoAdmin
from .profiles import (
    ProfileAdmin,
    ProfileGroupAdmin,
    ProfilePhotoAdmin,
)

from .shows import (
    ShowAdmin,
    ShowBandAdmin,
    ShowPhotoAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
    ShowTypePhotoAdmin,
)

from .theatre_sports import (
    FoulAdmin,
    FoulTypeAdmin,
    MatchAdmin,
    MatchStageAdmin,
    ScorePointAdmin,
)

__all__ = (
    'BandAdmin',
    'BandPhotoAdmin',
    'FoulAdmin',
    'FoulTypeAdmin',
    'GameAdmin',
    'GameRulesAdmin',
    'InspirationAdmin',
    'LocationAdmin',
    'LocationPhotoAdmin',
    'MatchAdmin',
    'MatchStageAdmin',
    'ProfileAdmin',
    'ProfileGroupAdmin',
    'ProfilePhotoAdmin',
    'ScorePointAdmin',
    'ShowAdmin',
    'ShowBandAdmin',
    'ShowPhotoAdmin',
    'ShowRoleAdmin',
    'ShowTypeAdmin',
    'ShowTypePhotoAdmin',
)
