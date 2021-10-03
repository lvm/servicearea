from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from world_class import Languages
from world_class import Currencies

from mozio.apps.utils.models import NamedMixinModel
from mozio.apps.utils.models import TimestampMixinModel


class Provider(NamedMixinModel, TimestampMixinModel, models.Model):
    LANG_CHOICES = ((l.code, l.name) for l in Languages())
    CURR_CHOICES = ((c.code, c.name) for c in Currencies())

    email = models.EmailField(_("Email"), max_length=255)
    phone_number = PhoneNumberField(_("Phone"), max_length=100)
    language = models.CharField(
        _("Language"), choices=LANG_CHOICES, default="en", max_length=2
    )
    currency = models.CharField(
        _("Currency"), choices=CURR_CHOICES, default="USD", max_length=4
    )

    class Meta:
        unique_together = ["name", "email"]
        ordering = ["-created_at", "-updated_at"]


class ServiceArea(NamedMixinModel, TimestampMixinModel, models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    area = gis_models.PolygonField()

    class Meta:
        ordering = ["-created_at", "-updated_at"]
