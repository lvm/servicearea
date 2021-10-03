from django.contrib import admin

from mozio.apps.providers.models import Provider
from mozio.apps.providers.models import ServiceArea


admin.site.register(Provider, admin.ModelAdmin)
admin.site.register(ServiceArea, admin.ModelAdmin)
