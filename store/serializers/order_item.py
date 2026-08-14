from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from . import ProductSerializer
from store.models import OrderItem, Order, Product
#from .order import OrderSerializer



class OrderItemSerializer(serializers.ModelSerializer):

    # order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):

    order = PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']
        read_only_fields = ['id']

    def validate_quantity(self, value):
        if value > 1000:
            raise serializers.ValidationError('Quantity above 1000 is not allowed!!')
        return value
