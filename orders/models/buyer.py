from django_countries.fields import CountryField
from django.db.models import CharField, EmailField, Model
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from django_extensions.db.models import TimeStampedModel

from fields import NameField


class OrderAddressModel(Model):

    class Meta:
        abstract = True

    country = CountryField()
    address = CharField(
        help_text=_('Physical world address'),
        max_length=255,
        verbose_name=_('Address'),
    )
    city = CharField(
        max_length=255,
        verbose_name=_('City'),
    )
    postal_code = CharField(
        help_text=_('Postal/ZIP code'),
        max_length=255,
        verbose_name=_('Postal code'),
    )


class OrderContact(OrderAddressModel, TimeStampedModel):

    class Meta:
        abstract = True

    name = NameField
    email = EmailField(
        verbose_name=_('E-mail address'),
        help_text=_('E-mail address to send the invoice'),
    )
    phone = PhoneNumberField(blank=True)


class Buyer(OrderContact):

    class Meta:
        verbose_name = _('Buyer')
        verbose_name_plural = _('Buyers')
