from django.db.models import PositiveIntegerField
from django.utils.translation import ugettext_lazy as _

POLL_TYPE_AUDIBLE = 1

POLL_TYPE_CHOICES = (
    (POLL_TYPE_AUDIBLE, _('Audible vote')),
)

class LivePollTypeField(PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = POLL_TYPE_CHOICES
        kwargs['default'] = POLL_TYPE_AUDIBLE
        kwargs['verbose_name'] = _('Poll Type')
        kwargs['help_text'] = _('pollTypeHelpText')
        super().__init__(*args, **kwargs)
