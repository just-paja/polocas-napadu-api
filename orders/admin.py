from fields.admin import BaseAdminModel, BaseInlineAdminModel

from .models import Buyer, DeliveryMethod, Order, OrderItem, PaymentMethod


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


class OrderItemAdmin(BaseInlineAdminModel):

    model = OrderItem
    extra = 0
    autocomplete_fields = ('product__show_ticket__show_ticket_price__show__name',)


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
