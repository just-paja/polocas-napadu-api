from django_extensions.db.models import AutoSlugField
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin

ANCHOR_HISTORY = 'history'

ANCHOR_CHOICES = [
    (ANCHOR_HISTORY, _('Group history')),
]


class Article(PublicResourceMixin):

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    slug = AutoSlugField(_('Slug'), populate_from='name')
    site_anchor = CharField(
        blank=True,
        choices=ANCHOR_CHOICES,
        max_length=31,
        null=True,
        unique=True,
        verbose_name=_('Site Anchor'),
    )
