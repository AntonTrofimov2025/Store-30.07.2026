from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
from store.models import (Category, Supplier, Product, Order,
                          ProductDetail, Address, Customer, OrderItem)
from store.serializers import (CategorySerializer, CategoryCreateSerializer,
                               SupplierSerializer, SupplierCreateSerializer,
                               ProductDetailSerializer, ProductDetailCreateUpdateSerializer,
                               ProductSerializer, AddressSerializer,
                               AddressCreateUpdateSerializer,
                               CustomerSerializer, CustomerCreateUpdateSerializer,
                               OrderSerializer, OrderCreateUpdateSerializer,
                               OrderItemSerializer, OrderItemCreateUpdateSerializer)
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import ProductFilter
from rest_framework.decorators import action
from django.db.models import Count, Q


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    serializers = {
        'POST': CategoryCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, CategorySerializer)

    @action(detail=False, methods=['get'], url_name='count', url_path='count')
    def count_all_categories(self, request, *args, **kwargs):
        count_all_cats = Category.objects.annotate(total_products=Count('products__id')).values('slug', 'total_products')
        result = {f'total_products_in_category_{category['slug'].replace('-', '_')}': category['total_products']
                  for category in count_all_cats}
        return Response(result, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['get'], url_name='count', url_path='count')
    # def count_all_categories(self, request, *args, **kwargs):
    #     count_all_cats = Category.objects.aggregate(
    #         **{f'total_products_in_category_{name['slug'].replace('-', '_')}': Count('products__id', filter=Q(name=name['name']))
    #            for name in Category.objects.values('name', 'slug')})
    #     return Response(count_all_cats, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['get'], url_name='count', url_path='count')
    # def count_all_categories(self, request, *args, **kwargs):
    #     count_all_cats = Category.objects.aggregate(
    #         **{f'total_products_in_category_{name['name'].lower().replace(' ', '_')}': Count('products__id', filter=Q(name=name['name']))
    #            for name in Category.objects.values('name')})
    #     return Response(count_all_cats, status=status.HTTP_200_OK)

class SupplierViewSet(viewsets.ModelViewSet):

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    serializers = {
        'POST': SupplierCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, SupplierSerializer)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.select_related('category', 'supplier').all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'price']
    filterset_class = ProductFilter


class ProductDetailViewSet(viewsets.ModelViewSet):

    queryset = ProductDetail.objects.select_related('product', 'product__category', 'product__supplier').all()
    serializer_class = ProductDetailSerializer

    serializers = {
        'POST': ProductDetailCreateUpdateSerializer,
        'PUT': ProductDetailCreateUpdateSerializer,
        'PATCH': ProductDetailCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, ProductDetailSerializer)


class AddressViewSet(viewsets.ModelViewSet):

    # queryset = Address.objects.prefetch_related('customers', 'customers__orders',
    #                                             'customers__orders__items') .all()
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    serializers = {
        'POST': AddressCreateUpdateSerializer,
        'PUT': AddressCreateUpdateSerializer,
        'PATCH': AddressCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, AddressSerializer)


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = (Customer.objects.select_related('address').
                prefetch_related('orders', 'orders__items', 'orders__items__product', 'orders__items__product__detail',
                                 'orders__items__product__category', 'orders__items__product__supplier'))
    serializer_class = CustomerSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']

    serializers = {
        'POST': CustomerCreateUpdateSerializer,
        'PUT': CustomerCreateUpdateSerializer,
        'PATCH': CustomerCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, CustomerSerializer)

    # def get_serializer_class(self):
    #     if self.action in ['create', 'update', 'partial_update']:
    #         return CustomerCreateUpdateSerializer
    #     return CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.select_related('customer').prefetch_related('items', 'items__product',
                                    'items__product__category', 'items__product__supplier', 'items__product__detail')
    serializer_class = OrderSerializer

    serializers = {
        'POST': OrderCreateUpdateSerializer,
        'PUT': OrderCreateUpdateSerializer,
        'PATCH': OrderCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, OrderSerializer)


class OrderItemViewSet(viewsets.ModelViewSet):

    queryset = OrderItem.objects.select_related('order', 'product',
                                                'product__category', 'product__detail', 'product__supplier')
    serializer_class = OrderItemSerializer

    serializers = {
        'POST': OrderItemCreateUpdateSerializer,
        'PUT': OrderItemCreateUpdateSerializer,
        'PATCH': OrderItemCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.request.method, OrderItemSerializer)

