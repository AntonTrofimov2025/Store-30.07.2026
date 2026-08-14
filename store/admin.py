from django.contrib import admin
from store.models import (Address, Category, Customer, Order,
                          OrderItem, Product, ProductDetail, Supplier)
from django.utils.translation import gettext_lazy as _



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['country', 'city', 'street', 'house']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_joined',
                    'show_is_deleted', 'deleted_at']
    search_fields = ['last_name', 'email']
    # list_filter = ['date_joined']

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
    list_display = ['customer', 'order_date']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return (queryset.select_related('customer', 'customer__address').
                prefetch_related('items__product', 'items__product__category', 'items__product__supplier'))

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
    list_display = ['name', 'category', 'supplier', 'price', 'quantity', 'article', 'available']

    inlines = [ProductDetailInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category', 'supplier')

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'description', 'manufacturing_date', 'expiration_date', 'weight']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'product__category', 'product__supplier')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'phone_number']

