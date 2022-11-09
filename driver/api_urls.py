from django.urls import path
from driver.views import NearDrivers


urlpatterns = [
        path(
            'near_drivers',
            NearDrivers.as_view()
        )
]