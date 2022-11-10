from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from order.serializers import CreateOrderSerializerRequest 
from order.serializers import GetOrdersByDateSerializerRequest 
from order.serializers import GetOrdersByDriverDatesSerializerRequest 
from order.serializers import CreateOrderSerializerResponse
from order.serializers import OrderDetailSerializerResponse
from order.services import OrderService


class CreateOrderView(APIView):
    
    @swagger_auto_schema(
        query_serializer=CreateOrderSerializerRequest,
        responses={
            200: CreateOrderSerializerResponse,
            status.HTTP_400_BAD_REQUEST:CreateOrderSerializerRequest,
            status.HTTP_412_PRECONDITION_FAILED:"Error"
            },
        tags=['Orders'],
    )
    def post(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        data = request.query_params.dict()
        serializer = CreateOrderSerializerRequest(data=data, context=serializer_context)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        new_order, message = OrderService().create_order(
            **serializer.data
        )
        if  new_order is None:
            return Response(
                message,
                status.HTTP_412_PRECONDITION_FAILED
            )

        return Response(
            CreateOrderSerializerResponse(
                new_order,
                context=serializer_context,
            ).data,
            status.HTTP_200_OK
        )
    
class ListOrdersView(APIView):
    
    @swagger_auto_schema(
        query_serializer=GetOrdersByDateSerializerRequest,
        responses={
            200: OrderDetailSerializerResponse(many=True),
            status.HTTP_400_BAD_REQUEST:GetOrdersByDateSerializerRequest,
            },
        tags=['Orders'],
    )
    def get(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        data = request.query_params.dict()
        serializer = GetOrdersByDateSerializerRequest(data=data, context=serializer_context)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        new_order = OrderService().get_orders_by_date(
            **serializer.data
        )

        return Response(
            OrderDetailSerializerResponse(
                new_order,
                context=serializer_context,
                many=True
            ).data,
            status.HTTP_200_OK
        )

class ListDriversOrdersView(APIView):

    @swagger_auto_schema(
        query_serializer=GetOrdersByDriverDatesSerializerRequest,
        responses={
            200: OrderDetailSerializerResponse(many=True),
            status.HTTP_400_BAD_REQUEST:GetOrdersByDateSerializerRequest,
            },
        tags=['Orders'],
    )
    def get(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        data = request.query_params.dict()
        serializer = GetOrdersByDriverDatesSerializerRequest(data=data, context=serializer_context)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        new_order = OrderService().get_orders_by_driver_and_date(
            **serializer.data
        )

        return Response(
            OrderDetailSerializerResponse(
                new_order,
                context=serializer_context,
                many=True
            ).data,
            status.HTTP_200_OK
        )

