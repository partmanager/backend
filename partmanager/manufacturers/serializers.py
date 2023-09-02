from .models import Manufacturer
from rest_framework import serializers


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id',
                  'name',
                  'full_name',
                  'website'
                  ]
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
