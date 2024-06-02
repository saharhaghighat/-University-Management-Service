from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RequestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "request"
    verbose_name =  _("request")
