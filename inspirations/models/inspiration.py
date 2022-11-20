from django.db.models import BooleanField, CharField, ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Inspiration(TimeStampedModel):
    class Meta:
        verbose_name = _("Inspiration")
        verbose_name_plural = _("Inspirations")

    show = ForeignKey("shows.Show", on_delete=CASCADE, related_name="inspirations")
    text = CharField(
        max_length=255,
        verbose_name=_("Textual inspiration"),
        help_text=_(
            "Enter words that will serve as an inspiration for this improvisation"
        ),
    )
    discarded = BooleanField(default=False)

    def get_show_name(self):
        return self.show.name

    def get_show_date(self):
        return self.show.start


Inspiration.get_show_date.short_description = _("Date")
Inspiration.get_show_name.short_description = _("Show")
