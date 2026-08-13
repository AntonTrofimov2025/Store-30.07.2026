from rest_framework import serializers
from store.models import Supplier



class SupplierSerializer(serializers.ModelSerializer):

    contact_email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_email', 'phone_number']
        read_only = ['id']

class SupplierCreateSerializer(serializers.ModelSerializer):

    contact_email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res = res.pop('id')

        return {'id': res}

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_email', 'phone_number']
        read_only = ['id']

