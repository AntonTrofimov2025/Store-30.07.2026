from rest_framework import serializers
# from .customer import CustomerSerializer
from store.models import Address



class AddressSerializer(serializers.ModelSerializer):
    # customers = CustomerSerializer(read_only=True, many=True)

    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'house', 'address_type']

class AddressCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'country', 'city', 'street', 'house', 'address_type']
        read_only_fields = ['id']

