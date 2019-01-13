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

__all__ = (
    'BandAdmin',
    'BandPhotoAdmin',
    'LocationAdmin',
    'LocationPhotoAdmin',
    'ProfileAdmin',
    'ProfileGroupAdmin',
    'ProfilePhotoAdmin',
    'ShowAdmin',
    'ShowBandAdmin',
    'ShowPhotoAdmin',
    'ShowRoleAdmin',
    'ShowTypeAdmin',
    'ShowTypePhotoAdmin',
)
