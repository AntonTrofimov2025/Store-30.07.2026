from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from store.models import Product
from . import SupplierSerializer, CategorySerializer
from store.models import Category, Supplier



class ProductSerializer(serializers.ModelSerializer):

    category_detail = CategorySerializer(source='category', read_only=True)
    supplier_detail = SupplierSerializer(source='supplier', read_only=True)

    category = PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    supplier = PrimaryKeyRelatedField(queryset=Supplier.objects.all(), write_only=True)

    # def to_representation(self, instance):
    #     res = super().to_representation(instance)
    #     res = res.pop('id')
    #
    #     return {'id': res}

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'article', 'quantity', 'available',
                  'category', 'supplier', 'category_detail', 'supplier_detail']
        read_only_fields = ['id']

