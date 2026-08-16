from django.db import models
from django.utils.translation import gettext_lazy as _


class AddressTypes(models.TextChoices):
    HOME = 'hm', _('Home')
    WORK = 'wk', _('Work')
    PICKUP = 'pp', _('Pickup point')

class CustomerTypes(models.TextChoices):
    NEW = 'nw', _('New')
    REGULAR = 'rg', _('Regular')
    VIP = 'vp', _('VIP')
    WHOLESALE = 'wh', _('Wholesale')

class SupplierStatus(models.TextChoices):
    ACTIVE = 'av', _('Active')
    SUSPENDED = 'sp', _('Suspended')
    IN_BLACK_LIST = 'bl', _('Blacklisted')

class ProductStatus(models.TextChoices):
    IN_STOCK = 'is', _('In stock')
    ON_DEMAND = 'od', _('On demand')
    AWAITED = 'aw', _('Awaited')
    DISCONTINUED = 'dc', _('Discontinued')
    REM_FROM_SALE = 'rm', _('Removed from sale')

class ProductDetailTypes(models.TextChoices):
    COMPACT = 'cp', _('Compact')
    BULKY = 'bk', _('Bulky')

class OrderStatus(models.TextChoices):
    PENDING = 'pn', _('Pending')
    PAID = 'pd', _('Paid')
    PROCESSING = 'pr', _('Processing')
    SHIPPED = 'sh', _('Shipped')
    DELIVERED = 'dl', _('Delivered')
    CANCELLED = 'cl', _('Cancelled')