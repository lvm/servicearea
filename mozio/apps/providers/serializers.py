from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from mozio.apps.providers.models import Provider
from mozio.apps.providers.models import ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ServiceAreaSerializer(gis_serializers.GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        geo_field = "area"
        fields = "__all__"
