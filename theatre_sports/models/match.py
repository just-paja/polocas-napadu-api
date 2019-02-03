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

    def get_current_stage(self):
        return self.stages.order_by('-created').first()

    def get_prev_stage(self):
        try:
            return self.stages.order_by('-created')[1]
        except IndexError:
            return None
