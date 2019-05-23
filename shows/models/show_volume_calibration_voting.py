from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from voting.models import LivePollVoting

class ShowVolumeCalibrationVoting(LivePollVoting):
    calibration = ForeignKey(
        'ShowVolumeCalibration',
        related_name='calibration_votings',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = _('Show volume calibration voting')
        verbose_name_plural = _('Show volume calibrations voting')
