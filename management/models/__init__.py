"""Import all models."""

from .bands import BandAdmin, BandPhotoAdmin
from .locations import LocationAdmin, LocationPhotoAdmin
from .profiles import ProfileAdmin, ProfilePhotoAdmin
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
    ProfilePhotoAdmin,
    ShowAdmin,
    ShowBandAdmin,
    ShowPhotoAdmin,
    ShowRoleAdmin,
    ShowTypeAdmin,
    ShowTypePhotoAdmin,
)
