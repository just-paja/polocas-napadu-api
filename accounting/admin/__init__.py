from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from eshop.admin import ShowTicketAdmin, ShowTicketPriceAdmin
from fields.admin import ImprovAdminSite
from orders.admin import (
    BuyerAdmin,
    DeliveryMethodAdmin,
    OrderAdmin,
    PaymentMethodAdmin,
)

from .account import AccountAdmin
from .counterparty import CounterPartyAdmin, KnownAccountAdmin
from .membership import MembershipAdmin, MembershipLevelAdmin
from .payments import PromiseAdmin, StatementAdmin
from .price_level import PriceLevelAdmin
from .purpose import PurposeAdmin, PurposeCategoryAdmin


class AccountingAdminSite(ImprovAdminSite):
    name = 'accounting'
    site_title = _('Accounting')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookup(AccountAdmin)
        self.hookup(BuyerAdmin)
        self.hookup(CounterPartyAdmin)
        self.hookup(DeliveryMethodAdmin)
        self.hookup(KnownAccountAdmin)
        self.hookup(MembershipAdmin)
        self.hookup(MembershipLevelAdmin)
        self.hookup(OrderAdmin)
        self.hookup(PaymentMethodAdmin)
        self.hookup(PriceLevelAdmin)
        self.hookup(PromiseAdmin)
        self.hookup(PurposeAdmin)
        self.hookup(PurposeCategoryAdmin)
        self.hookup(ShowTicketAdmin)
        self.hookup(ShowTicketPriceAdmin)
        self.hookup(StatementAdmin)
        self.register(auth_admin.User, auth_admin.UserAdmin)


ACCOUNTING_ADMIN = AccountingAdminSite()
