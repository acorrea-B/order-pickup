from django.contrib import admin
from driver import api_urls
from django.urls import path
from django.urls import include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Wash my car",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', 
        include([
            path('driver/', include(api_urls.urlpatterns)),
            path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
        ])
    ),
]
