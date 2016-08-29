"""This module contains declarations of models that are registered to
appear in the `Admin` panels.

"""

from django.contrib import admin
from update.models import InstrumentMap

admin.site.register(InstrumentMap)
