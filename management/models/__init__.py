"""Import all models."""

from .bands import BandAdmin, BandPhotoAdmin
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
