from rest_framework import serializers
from store.models import Category



class CategoryCreateSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res = res.pop('id')

        return {'id': res}

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only = ['id']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

