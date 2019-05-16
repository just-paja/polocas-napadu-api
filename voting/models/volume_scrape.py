from django.db.models import FloatField, ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .live_poll_voting import LivePollVoting

class VolumeScrape(TimeStampedModel):
    vote = ForeignKey(
        'LivePollVoting',
        on_delete=CASCADE,
        related_name='volume_scrapes',
        verbose_name=_('Live Poll Voting'),
    )
    volume = FloatField(
        verbose_name=_('Recorded volume'),
    )

    class Meta:
        verbose_name = _('Volume scrape')
        verbose_name_plural = _('Volume scrapes')

    def clean(self, *args, **kwargs):
        if self.vote.closed:
            raise LivePollVoting.AlreadyClosed(
                'Poll %s is already closed' % self.vote.pk
            )
