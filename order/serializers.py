from rest_framework import serializers

from driver.serializers import NearDriverSerializerResponse
from driver.models import Driver
from order.models import Order

class CreateOrderSerializerRequest(serializers.Serializer):
    driver = serializers.IntegerField(min_value=0)
    lat_origin = serializers.IntegerField(max_value=100)
    lng_origin = serializers.IntegerField(max_value=100)
    lat_destination = serializers.IntegerField(max_value=100)
    lng_destination = serializers.IntegerField(max_value=100)
    order_date = serializers.DateTimeField()

    def validate_driver(self, value):
        try:
            Driver.objects.get(id=value)
        except Driver.DoesNotExist:
            raise serializers.ValidationError("El conductor ingresado no existe")
        return value

class GetOrdersByDateSerializerRequest(serializers.Serializer):
    date = serializers.DateField(format="%Y-%m-%d")

class GetOrdersByDriverDatesSerializerRequest(serializers.Serializer):
    date = serializers.DateField(format="%Y-%m-%d")
    driver = serializers.IntegerField(min_value=0)

    def validate_driver(self, value):
        try:
            Driver.objects.get(id=value)
        except Driver.DoesNotExist:
            raise serializers.ValidationError("El conductor ingresado no existe")
        return value

class CreateOrderSerializerResponse(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_date', 'creation_date')


class OrderDetailSerializerResponse(serializers.HyperlinkedModelSerializer):
    driver = NearDriverSerializerResponse(read_only=True)
    class Meta:
        model = Order
        fields = (
            'driver', 'creation_date',
            'order_date', 'lat_origin',
            'lng_origin', 'lat_destination',
            'lng_destination'
        )
        