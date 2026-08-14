from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from store.models import ProductDetail, Product
from . import ProductSerializer

class ProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductDetail
        fields = ['description', 'product', 'manufacturing_date', 'expiration_date', 'weight']

class ProductDetailCreateUpdateSerializer(serializers.ModelSerializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = ProductDetail
        fields = ['id', 'description', 'product', 'manufacturing_date', 'expiration_date', 'weight']
        read_only_fields = ['id']