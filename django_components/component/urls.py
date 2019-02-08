"""
Components urls

These URL are generated on the fly, by readint the Component table.

These components should exist before django start, because urlpatterns are created when starting the server.
If a new component is added, it will not be serve until the server restarts.
"""
import logging

from django.core.exceptions import ViewDoesNotExist
from django.core.management import color_style
from django.db import OperationalError
from django.utils.translation import ugettext as _
from component.models import Component
from django.urls import path



logger = logging.getLogger("django")
style = color_style()

urlpatterns = [] # pylint: disable=invalid-name

try:
    for component in Component.objects.all():
        try:
            urlpatterns.append(component.url_pattern)
        except ViewDoesNotExist as e:
            logger.info(style.WARNING("{}, please check component named '{}'.".format(e, component.name)))
except OperationalError as e:
    logger.info(style.WARNING(str(e) + "\n\n" + _("This can be normal (if the db is not set yet, for instance).")))
