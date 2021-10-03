from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include

title = "%s (%s)" % (settings.ADMIN_TITLE, settings.ENV_NAME)
admin.site.site_header = title
admin.site.site_title = title

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("mozio.apps.providers.urls")),
]
