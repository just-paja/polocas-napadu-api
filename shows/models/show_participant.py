from django_extensions.db.models import TimeStampedModel
from django.db.models import ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _


class ShowParticipant(TimeStampedModel):

    class Meta:
        verbose_name = _('Show participant')
        verbose_name_plural = _('Show participants')

    show = ForeignKey(
        'Show',
        on_delete=CASCADE,
        related_name='showsParticipants',
        verbose_name=_('Show'),
    )
    profile = ForeignKey(
        'profiles.Profile',
        on_delete=CASCADE,
        related_name='showsParticipated',
        verbose_name=_('Profile'),
    )
    role = ForeignKey(
        'ShowRole',
        on_delete=CASCADE,
        related_name='showsParticipants',
        verbose_name=_('Role'),
    )

    def __str__(self):
        return self.profile.name

    def get_show_name(self):
        return self.show.name

    def get_show_date(self):
        return self.show.start


ShowParticipant.get_show_date.short_description = _('Date')
ShowParticipant.get_show_name.short_description = _('Show')
