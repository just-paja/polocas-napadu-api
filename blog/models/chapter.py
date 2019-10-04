from django_extensions.db.models import AutoSlugField
from django.db.models import ForeignKey, IntegerField, CASCADE
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class Chapter(PublicResourceMixin):

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')

    article = ForeignKey(
        'Article',
        on_delete=CASCADE,
    )
    slug = AutoSlugField(_('Slug'), populate_from='name')
    weight = IntegerField(
        default=0,
        help_text=_('weightHelpText'),
        verbose_name=_('Weight'),
    )
