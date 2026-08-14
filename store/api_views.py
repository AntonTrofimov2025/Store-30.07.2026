from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from store.models import (Category, Supplier, Product, ProductDetail,
                          Address, Customer, Order, OrderItem)
from .serializers import (CategorySerializer, SupplierSerializer,
                          ProductSerializer, CategoryCreateSerializer,
                          SupplierCreateSerializer, ProductDetailSerializer,
                          ProductDetailCreateUpdateSerializer, AddressSerializer,
                          AddressCreateUpdateSerializer, CustomerSerializer,
                          CustomerCreateUpdateSerializer,
                          OrderSerializer, OrderItemSerializer,
                          OrderItemCreateUpdateSerializer,
                          OrderCreateUpdateSerializer)


class CategoryListAPIView(ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer


class SupplierListAPIView(ListCreateAPIView):

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SupplierCreateSerializer
        return SupplierSerializer


class ProductListAPIView(ListCreateAPIView):

    queryset = Product.objects.select_related('category', 'supplier').all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.select_related('category', 'supplier').all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


class ProductDetailListAPIView(ListCreateAPIView):

    queryset = ProductDetail.objects.select_related('product', 'product__category', 'product__supplier').all()
    serializer_class = ProductDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductDetailCreateUpdateSerializer
        return ProductDetailSerializer

class ProductDetailDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductDetail.objects.select_related('product', 'product__category', 'product__supplier').all()
    serializer_class = ProductDetailSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductDetailCreateUpdateSerializer
        return ProductDetailSerializer


class AddressListAPIView(ListCreateAPIView):
    queryset = Address.objects.prefetch_related('customers', 'customers__orders',
                                                'customers__orders__items') .all()
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddressCreateUpdateSerializer
        return AddressSerializer

class AddressDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.prefetch_related('customers', 'customers__orders',
                                                'customers__orders__items').all()
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AddressCreateUpdateSerializer
        return AddressSerializer

class CustomerListAPIView(ListCreateAPIView):
    queryset = (Customer.objects.select_related('address').
                prefetch_related('orders', 'orders__items', 'orders__items__product', 'orders__items__product__detail',
                                 'orders__items__product__category', 'orders__items__product__supplier'))
    serializer_class = CustomerSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerCreateUpdateSerializer
        return CustomerSerializer

class CustomerDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = (Customer.objects.select_related('address').
                prefetch_related('orders', 'orders__items', 'orders__items__product', 'orders__items__product__detail',
                                 'orders__items__product__category', 'orders__items__product__supplier'))
    serializer_class = CustomerSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CustomerCreateUpdateSerializer
        return CustomerSerializer


class OrderListAPIView(ListCreateAPIView):
    queryset = Order.objects.select_related('customer').prefetch_related('items', 'items__product',
                                    'items__product__category', 'items__product__supplier', 'items__product__detail')
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateUpdateSerializer
        return OrderSerializer


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related('customer').prefetch_related('items', 'items__product',
                                    'items__product__category', 'items__product__supplier', 'items__product__detail')
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderCreateUpdateSerializer
        return OrderSerializer


class OrderItemListAPIView(ListCreateAPIView):
    queryset = OrderItem.objects.select_related('order', 'product',
                                                'product__category', 'product__detail', 'product__supplier')
    serializer_class = OrderItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer


class OrderItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.select_related('order', 'product',
                                                'product__category', 'product__detail', 'product__supplier')
    serializer_class = OrderItemSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer

