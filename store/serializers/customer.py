from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from store.models import Customer, Address
from .address import AddressSerializer
from .order import OrderSerializer
import re


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    orders = OrderSerializer(read_only=True, many=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'is_deleted',
                  'phone_number', 'address', 'orders', 'date_joined',
                  'customer_type']
        read_only_fields = ['date_joined', 'is_deleted', 'deleted_at']


class CustomerCreateUpdateSerializer(serializers.ModelSerializer):
    address = PrimaryKeyRelatedField(queryset=Address.objects.all(), write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone_number', 'address', 'customer_type']
        read_only_fields = ['id', 'date_joined', 'is_deleted', 'deleted_at']

    def validate_phone_number(self, value):
        if not re.match(r'^\+\d{10,14}$', value):
            raise serializers.ValidationError('The phone number must consist of 10-15 symbols in total and start from + symbol!!\n'
                                              'Example: +3423234455323')
        return value

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('This email already exists!!')
        return value

    # def create(self, validated_data):
    #     if Customer.objects.filter(email=validated_data.get('email')).exists():
    #         raise serializers.ValidationError('This email already exists!!')
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     email = validated_data.get('email')
    #     if email and Customer.objects.filter(email=email).exclude(pk=instance.pk).exists():
    #         raise serializers.ValidationError('This email already exists!!')
    #     return super().update(instance, validated_data)
    #

