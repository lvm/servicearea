from world_class import Languages
from world_class import Currencies

from rest_framework import viewsets
from rest_framework.response import Response

from mozio.apps.providers.models import Provider
from mozio.apps.providers.models import ServiceArea
from mozio.apps.providers.serializers import ProviderSerializer
from mozio.apps.providers.serializers import ServiceAreaSerializer


class LanguageViewSet(viewsets.ViewSet):
    def list(self, request):
        languages = [l.as_dict() for l in Languages()]
        return Response(languages)

class CurrencyViewSet(viewsets.ViewSet):
    def list(self, request):
        currencies = [c.as_dict() for c in Currencies()]
        return Response(currencies)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
