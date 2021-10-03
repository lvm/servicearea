import logging

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class ProvidersConfig(AppConfig):
    name = "mozio.apps.utils"
    verbose_name = _("Utilities")
    description = _("Utilities")
