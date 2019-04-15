from django.utils.translation import ugettext_lazy as _

from fields import PublicResourceMixin


class ShowType(PublicResourceMixin):
    class Meta:
        verbose_name = _('Show type')
        verbose_name_plural = _('Show types')
