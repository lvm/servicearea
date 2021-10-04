from django.conf import settings
from django.urls import path
from django.urls import include
from django.urls import re_path


from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Service Area API",
        default_version="v1",
        description="This is a toy-project to test the capabilities of DRF Gis",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="legal@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path("api/login/", obtain_auth_token, name="api_token_auth"),
    path("api/", include("mozio.apps.providers.urls")),
    re_path(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
