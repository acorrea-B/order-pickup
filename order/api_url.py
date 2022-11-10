from django.urls import path
from order.views import CreateOrderView
from order.views import ListOrdersView
from order.views import ListDriversOrdersView


urlpatterns = [
        path(
            'create',
            CreateOrderView.as_view(),
        ),
        path(
            '',
            ListOrdersView.as_view(),  
        ),
        path(
            'driver',
            ListDriversOrdersView.as_view(),  
        ),
]