from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import (
    Buyer,
    DeliveryMethod,
    Order,
    Orderable,
    OrderItem,
    PaymentMethod,
)


class DeliveryMethodAdmin(BaseAdminModel):

    model = DeliveryMethod
    search_fields = ('name', 'description')


class PaymentMethodAdmin(BaseAdminModel):

    model = PaymentMethod
    search_fields = ('name', 'description')


class BuyerAdmin(BaseAdminModel):

    model = Buyer
    search_fields = (
        'name',
        'country',
        'address',
        'city',
        'postal_code',
    )


class OrderableAdmin(BaseAdminModel):
    model = Orderable
    search_fields = (
        'showticket__show_ticket_price__show__name',
        'showticket__show_ticket_price__price_level__name',
        'showticket__show_ticket_price__price',
        'showticket__show_ticket_price__currency',
    )


class OrderItemAdmin(BaseInlineAdminModel):

    model = OrderItem
    extra = 0
    autocomplete_fields = ('product',)


class OrderAdmin(BaseAdminModel):

    model = Order
    change_form_template = 'admin/order_change_form.html'
    inlines = [OrderItemAdmin]
    autocomplete_fields = (
        'buyer',
        'payment_method',
        'delivery_method',
        'promise',
        'owner',
    )
    fields = (
        'ident',
        'status',
        'buyer',
        'promise',
        'payment_method',
        'delivery_method',
        'owner',
    )
    readonly_fields = ('ident',)
