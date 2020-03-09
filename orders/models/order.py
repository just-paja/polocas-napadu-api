import datetime

from django.db.models import ForeignKey, PositiveSmallIntegerField, PositiveIntegerField, PROTECT
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

STATUS_READY = 1
STATUS_CANCELED = 2
STATUS_ORDERED = 3
STATUS_PAID = 4
STATUS_DELIVERED = 5

STATUS_CHOICES = (
    (STATUS_READY, _('Ready')),
    (STATUS_CANCELED, _('Canceled')),
    (STATUS_ORDERED, _('Ordered')),
    (STATUS_PAID, _('Paid')),
    (STATUS_DELIVERED, _('Delivered')),
)


class Order(TimeStampedModel):
    buyer = ForeignKey(
        'Buyer',
        verbose_name=_('Buyer'),
        help_text=_('The entity buying thes product'),
        on_delete=PROTECT,
    )
    payment_method = ForeignKey(
        'PaymentMethod',
        verbose_name=_('Payment method'),
        on_delete=PROTECT,
    )
    delivery_method = ForeignKey(
        'DeliveryMethod',
        verbose_name=_('Delivery method'),
        on_delete=PROTECT,
    )
    promise = ForeignKey(
        'accounting.Promise',
        verbose_name=_('Promise'),
        on_delete=PROTECT,
    )
    owner = ForeignKey(
        'auth.User',
        blank=True,
        help_text=_('Owner of this order'),
        on_delete=PROTECT,
        verbose_name=_('Owner'),
        null=True,
    )
    status = PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
        help_text=_('The current status of the order'),
        default=STATUS_READY,
    )
    ident = PositiveIntegerField(
        help_text=_('Unique identificator of the order'),
        unique=True,
        verbose_name=_('Order number'),
    )


    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.ident:
            today = datetime.date.today()
            last = self.__class__.objects.order_by('-ident').first()
            self.ident = int('%s%s' % (today.year, last.ident + 1))
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.ident)
