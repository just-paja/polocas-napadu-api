from django.db.models import BooleanField, Model, OneToOneField, CASCADE
from django.utils.translation import ugettext_lazy as _


class Match(Model):

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    show = OneToOneField(
        'shows.Show',
        on_delete=CASCADE,
        related_name='match',
    )
    closed = BooleanField(
        default=False,
    )

    def __str__(self):
        return '%s: %s' % (_('Match'), self.show)
