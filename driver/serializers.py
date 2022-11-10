from rest_framework import serializers
from driver.models import  Driver

class NearDriverSerializerRequest(serializers.Serializer):
    point = serializers.IntegerField(max_value=100)
    date = serializers.DateTimeField()


class NearDriverSerializerResponse(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'lat', 'lng')


