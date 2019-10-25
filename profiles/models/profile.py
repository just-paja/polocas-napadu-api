from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField, ForeignKey, ImageField, TextField, PROTECT
from django.utils.translation import ugettext_lazy as _

from fields import NameMixin, VisibilityMixin


class Profile(NameMixin, TimeStampedModel, VisibilityMixin):

    class Meta:
        verbose_name = _('Actor profile')
        verbose_name_plural = _('Actor profiles')

    alias = CharField(
        blank=True,
        max_length=63,
        null=True,
        help_text=_('artistAliasHelpText'),
        verbose_name=_('Artist alias'),
    )
    slug = AutoSlugField(_('Slug'), overwrite=True, populate_from='name')
    about = TextField()
    group = ForeignKey(
        'ProfileGroup',
        blank=True,
        null=True,
        on_delete=PROTECT,
    )
    avatar = ImageField(
        blank=True,
        null=True,
        upload_to='var/avatars',
        verbose_name=_('Avatar'),
    )

    def __str__(self):
        if self.alias:
            return '%s (%s)' % (self.alias, self.name)
        return super().__str__()
