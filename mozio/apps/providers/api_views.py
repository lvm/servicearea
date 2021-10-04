from world_class import Languages
from world_class import Currencies

from django.contrib.gis.geos import Point

from rest_framework import viewsets
from rest_framework.response import Response

from mozio.apps.providers.models import Provider
from mozio.apps.providers.models import ServiceArea
from mozio.apps.providers.serializers import ProviderSerializer
from mozio.apps.providers.serializers import ServiceAreaSerializer


class LanguageViewSet(viewsets.ViewSet):
    """
    This view is a READ-ONLY view that will always return a list of Languages.
    """
    def list(self, request):
        languages = [lang.as_dict() for lang in Languages()]
        return Response(languages)


class CurrencyViewSet(viewsets.ViewSet):
    """
    This view is a READ-ONLY view that will always return a list of Currencies.
    """
    def list(self, request):
        currencies = [curr.as_dict() for curr in Currencies()]
        return Response(currencies)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    def get_queryset(self):
        """
        This particular view receives 3 query params:

        As a pair:
        * coords={lat},{lng}
        Or Single QP
        * lat={lat}
        * lng={lng}

        These params will be converted to a `Point(lat,lng)`,
        which will be used to query if this particular point itersects
        with the all of the Polygons stored in db.
        """
        qs = super().get_queryset()
        if (
            self.request.query_params.get("coords", None)
            or self.request.query_params.get("lat", None)
            and self.request.query_params.get("lng", None)
        ):
            params = self.request.query_params
            if params.get("coords", None):
                lang, lng = [_.strip() for _ in params.get("coords").split(",")]
            else:
                lat = params.get("lat").strip()
                lng = params.get("lng").strip()

            qs = qs.filter(area__intersects=Point(float(lat), float(lng)))

        return qs
