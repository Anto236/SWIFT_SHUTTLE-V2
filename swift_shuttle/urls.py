from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# ✅ Configure Bearer Authentication for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Swift School Shuttle API",
        default_version='v1',
        description="API for managing school bus transportation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
authentication_classes=[JWTAuthentication, SessionAuthentication, BasicAuthentication],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # ✅ Swagger UI (Now supports Bearer Token)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
