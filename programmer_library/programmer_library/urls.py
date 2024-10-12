from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from programmer_library.views import redirect_to_api

schema_view = get_schema_view(
    openapi.Info(
        title='Library API',
        default_version='v1',
        description='API documentation for Library project',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@library.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', redirect_to_api),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc')
]
