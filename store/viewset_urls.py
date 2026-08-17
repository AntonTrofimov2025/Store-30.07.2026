from django.urls import path, include
from rest_framework.routers import SimpleRouter
from store.viewset_views import (CategoryViewSet, SupplierViewSet,
                                 ProductViewSet, ProductDetailViewSet,
                                 AddressViewSet, CustomerViewSet,
                                 OrderViewSet, OrderItemViewSet)


router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('suppliers', SupplierViewSet, basename='supplier')
router.register('products', ProductViewSet, basename='product')
router.register('product_details', ProductDetailViewSet, basename='product_detail')
router.register('addresses', AddressViewSet, basename='address')
router.register('customers', CustomerViewSet, basename='customer')
router.register('orders', OrderViewSet, basename='order')
router.register('order_items', OrderItemViewSet, basename='order_item')



urlpatterns = [
    path('', include(router.urls))
]

