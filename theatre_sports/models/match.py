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
        verbose_name=_('Closed'),
    )

    def __str__(self):
        return '%s: %s' % (_('Match'), self.show)

    def get_show_name(self):
        return self.show.name

    def get_show_date(self):
        return self.show.start

    def get_actual_start(self):
        first_stage = self.stages.order_by('created').first()
        return first_stage.created if first_stage else self.start

    def get_current_stage(self):
        return self.stages.order_by('-created').first()

    def get_prev_stage(self):
        try:
            return self.stages.order_by('-created')[1]
        except IndexError:
            return None

    def get_current_game(self):
        stage = self.get_current_stage()
        return stage.game

    def get_current_stage_name(self):
        stage = self.get_current_stage()
        if stage:
            return stage.get_type_display()
        return None


Match.get_show_name.short_description = _('Match')
Match.get_show_date.short_description = _('Date')
Match.get_current_stage_name.short_description = _('Stage')
