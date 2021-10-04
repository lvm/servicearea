import coreapi

from world_class import Languages
from world_class import Currencies


from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from mozio.apps.providers.models import Provider
from mozio.apps.providers.models import ServiceArea
from mozio.apps.providers.serializers import ProviderSerializer
from mozio.apps.providers.serializers import ServiceAreaSerializer


class CoordsFilterBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(name="lat", location="query", required=False, type="float"),
            coreapi.Field(name="lng", location="query", required=False, type="float"),
        ]


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

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    filter_backends = (CoordsFilterBackend,)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        """
        Service Area query parameters.

        This view accepts these Query Params:
        * `lat={lat}`
        * `lng={lng}`

        Alternatively you can pass both params at once:
        * `coords={lat},{lng}`

        These params will be converted to a `Point(lat,lng)`,
        which will be used to query if this particular point itersects
        with the all of the Polygons stored in db.

        `GET /api/serviceareas/?lat=-57.667236328124964&lng=-51.33747566296519`
        `GET /api/serviceareas/?coords=-57.667236328124964,-51.33747566296519`
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
