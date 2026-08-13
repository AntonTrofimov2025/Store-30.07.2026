from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from store.models import Category, Supplier, Product
from .serializers import (CategorySerializer, SupplierSerializer,
                          ProductSerializer, CategoryCreateSerializer,
                          SupplierCreateSerializer)



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

