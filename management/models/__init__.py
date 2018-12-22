"""Import all models."""

from .bands import BandAdmin, BandPhotoAdmin
from .locations import LocationAdmin, LocationPhotoAdmin
from .profiles import (
    ProfileAdmin,
    ProfileGroupAdmin,
    ProfilePhotoAdmin,
)

from .shows import (
    MatchResultsAdmin,
    MatchScoreAdmin,
    ShowAdmin,
    ShowBandAdmin,
    ShowPhotoAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
    ShowTypePhotoAdmin,
)

__all__ = (
    BandPhotoAdmin,
    LocationPhotoAdmin,
    MatchResultsAdmin,
    MatchScoreAdmin,
    ProfileAdmin,
    ProfileGroupAdmin,
    ProfilePhotoAdmin,
    ShowAdmin,
    ShowBandAdmin,
    ShowPhotoAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
    ShowTypePhotoAdmin,
)
