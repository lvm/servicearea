from django.urls import path

from rest_framework import routers

from mozio.apps.providers.api_views import ProviderViewSet
from mozio.apps.providers.api_views import ServiceAreaViewSet
from mozio.apps.providers.api_views import LanguageViewSet
from mozio.apps.providers.api_views import CurrencyViewSet

router = routers.SimpleRouter()
router.register(r"providers", ProviderViewSet)
router.register(r"serviceareas", ServiceAreaViewSet)


urlpatterns = [
    path("", LanguageViewSet.as_view({"get": "list"})),
    path("languages/", LanguageViewSet.as_view({"get": "list"})),
    path("currencies/", CurrencyViewSet.as_view({"get": "list"})),
]
urlpatterns += router.urls
