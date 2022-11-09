from multiprocessing import context
from driver.serializers import NearDriverSerializerResponse 
from driver.serializers import NearDriverSerializerRequest
from driver.services import DriverService
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class NearDrivers(APIView):

    @swagger_auto_schema(
        query_serializer=NearDriverSerializerRequest,
        responses={
            200: NearDriverSerializerResponse(many=True),
            status.HTTP_400_BAD_REQUEST:NearDriverSerializerRequest,
            },
        tags=['Drivers'],
    )
    def get(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        data = {
            'point':request.query_params.get('point'),
            'date':request.query_params.get('date')
        }

        serializer = NearDriverSerializerRequest(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        near_drivers = DriverService().get_nearest_driver(
            **serializer.data
        )
        return Response(
            NearDriverSerializerResponse(
                near_drivers,
                context=serializer_context,
                many=True
            ).data,
            status.HTTP_200_OK
        )


