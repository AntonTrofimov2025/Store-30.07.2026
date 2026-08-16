from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from store.models import Order, Customer
from .order_item import OrderItemSerializer
# from .customer import CustomerSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    # customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['order_date', 'items', 'status']


class OrderCreateUpdateSerializer(serializers.ModelSerializer):

    customer = PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'customer', 'status']
        read_only_fields = ['id', 'order_date']



