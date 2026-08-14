"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import info_
from .api_views import (CategoryListAPIView, SupplierListAPIView,
                        ProductListAPIView, ProductDetailAPIView,
                        ProductDetailListAPIView, ProductDetailDetailAPIView,
                        AddressListAPIView, AddressDetailAPIView,
                        CustomerListAPIView, CustomerDetailAPIView,
                        OrderListAPIView, OrderItemListAPIView,
                        OrderItemDetailAPIView, OrderDetailAPIView)

urlpatterns = [
    path('', info_, name='info'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list-create-view'),
    path('suppliers/', SupplierListAPIView.as_view(), name='supplier-list-create-view'),
    path('products/', ProductListAPIView.as_view(), name='product-list-create-view'),
    path('products/<int:pk>', ProductDetailAPIView.as_view(), name='product-detail-view'),
    path('product_details/', ProductDetailListAPIView.as_view(), name='prod_dt-list-create-view'),
    path('product_details/<int:pk>', ProductDetailDetailAPIView.as_view(), name='prod_dt-detail-view'),
    path('addresses/', AddressListAPIView.as_view(), name='address-list-create-view'),
    path('addresses/<int:pk>', AddressDetailAPIView.as_view(), name='address-detail-view'),
    path('customers/', CustomerListAPIView.as_view(), name='customer-list-create-view'),
    path('customers/<int:pk>', CustomerDetailAPIView.as_view(), name='customer-detail-view'),
    path('orders/', OrderListAPIView.as_view(), name='order-list-create-view'),
    path('orders/<int:pk>', OrderDetailAPIView.as_view(), name='order-detail-create-view'),
    path('order_items/', OrderItemListAPIView.as_view(), name='order_item-list-create-view'),
    path('order_items/<int:pk>', OrderItemDetailAPIView.as_view(), name='order_item-detail-view')
]
