"""This module contains declarations of models that are registered to
appear in the `Admin` panels.

"""

from django.contrib import admin
from update.models import InstrumentMap

class InstrumentMapAdmin(admin.ModelAdmin):
    list_display = ('raw_instrument', 'instrument')

admin.site.register(InstrumentMap, InstrumentMapAdmin)
