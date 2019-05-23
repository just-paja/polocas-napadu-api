from django.db.models import BooleanField, FloatField, ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class ShowVolumeCalibration(TimeStampedModel):
    show = ForeignKey(
        'Show',
        verbose_name=_('Show'),
        related_name='volume_calibrations',
        on_delete=CASCADE,
    )
    min = FloatField(
        null=True,
        blank=True,
        verbose_name=_('Minimum volume'),
        help_text=_('minimalAudioHelpText'),
    )
    mid = FloatField(
        null=True,
        blank=True,
        verbose_name=_('Medium volume'),
        help_text=_('mediumAudioHelpText'),
    )
    max = FloatField(
        null=True,
        blank=True,
        verbose_name=_('Maximum volume'),
        help_text=_('maximumAudioHelpText'),
    )
    closed = BooleanField(
        default=False,
        verbose_name=_('Closed'),
    )

    class Meta:
        verbose_name = _('Show volume calibration')
        verbose_name_plural = _('Show volume calibrations')

    def close(self):
        votings = self.calibration_votings.order_by('avg_volume')
        total = votings.count()
        sum = votings.aggregate(Sum('avg_volume')).values()[0]
        first = votings.first()
        last = votings.last()
        self.max = last.volume
        if first == last:
            self.min = 0
            self.mid = sum/2
        else:
            self.min = first.volume
            self.mid = sum/total
        self.save()
