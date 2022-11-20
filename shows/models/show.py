from django.db.models import BooleanField, ForeignKey, PROTECT
from django.utils.translation import gettext_lazy as _

from events.models import Event


class Show(Event):
    class Meta:
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")

    show_type = ForeignKey(
        "ShowType",
        on_delete=PROTECT,
        related_name="shows",
        verbose_name=_("Show type"),
    )
    use_inspirations = BooleanField(
        default=True,
        verbose_name=_('Use inspirations'),
        help_text=_("""
            Show will appear in the inspirations app and audience will be
            allowed to put in suggestions for the improv scenes
        """),
    )
