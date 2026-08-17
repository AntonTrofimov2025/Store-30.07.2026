from django.contrib import admin
from store.models import (Address, Category, Customer, Order,
                          OrderItem, Product, ProductDetail, Supplier)
from django.utils.translation import gettext_lazy as _
from core.models import (AddressTypes, CustomerTypes, SupplierStatus,
                         ProductStatus, ProductDetailTypes, OrderStatus)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['country', 'city', 'street', 'house', 'address_type']

    # @admin.action(description='Change address type to WORK')
    # def change_type_to_work(self, request, addresses):
    #     # for address in addresses:
    #     #     address.address_type = AddressTypes.WORK
    #     #     # address.save()
    #     # addresses.bulk_update(addresses, ['address_type'])
    #     addresses.update(address_type=AddressTypes.WORK)

    actions = [
        # change_type_to_work
              ]

    for add_type in AddressTypes:
        func = lambda self, request, addresses, v=add_type.value: addresses.update(address_type=v)
        func.short_description = f'Change Address Type to {add_type.label}'
        func.__name__ = add_type.name
        actions.append(func)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'customer_type',
                    'date_joined', 'show_is_deleted', 'deleted_at']
    search_fields = ['last_name', 'email']
    # list_filter = ['date_joined']

    actions = []

    for cust_type in CustomerTypes:
        func = lambda self, request, customers, v=cust_type.value: customers.update(customer_type=v)
        func.short_description = f'Change Customer Type to {cust_type.label}'
        func.__name__ = cust_type.name
        actions.append(func)

    @admin.display(boolean=True, description=_('Deleted?'))
    def show_is_deleted(self, obj):
        return obj.is_deleted

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('address')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2
    # raw_id_fields = ['product']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('order', 'order__customer', 'product', 'product__category', 'product__supplier')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_date', 'status']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return (queryset.select_related('customer', 'customer__address').
                prefetch_related('items__product', 'items__product__category', 'items__product__supplier'))

    actions = []

    for status in OrderStatus:
        func = lambda self, request, orders, v=status.value: orders.update(status=v)
        func.short_description = f'Change Order Status to {status.label}'
        func.__name__ = status.name
        actions.append(func)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('order', 'order__customer', 'product', 'product__category', 'product__supplier')

class ProductDetailInline(admin.StackedInline):
    model = ProductDetail

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'supplier', 'price', 'quantity', 'article', 'available',
                    'status']

    inlines = [ProductDetailInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category', 'supplier')

    actions = []

    for status in ProductStatus:
        func = lambda self, request, products, v=status.value: products.update(status=v)
        func.short_description = f'Change Product Status to {status.label}'
        func.__name__ = status.name
        actions.append(func)

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'description', 'manufacturing_date', 'expiration_date', 'weight',
                    'pd_type']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'product__category', 'product__supplier')

    actions = []

    for type_ in ProductDetailTypes:
        func = lambda self, request, product_details, v=type_.value: product_details.update(pd_type=v)
        func.short_description = f'Change ProductDetail Type to {type_.label}'
        func.__name__ = type_.name
        actions.append(func)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'phone_number', 'status']

    actions = []

    for status in SupplierStatus:
        func = lambda self, request, suppliers, v=status.value: suppliers.update(status=v)
        func.short_description = f'Change Supplier Status to {status.label}'
        func.__name__ = status.name
        actions.append(func)

