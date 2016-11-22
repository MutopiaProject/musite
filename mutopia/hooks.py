"""GITHUB hooks (webhooks)
This is a template. If hooks aren't used, this can be removed.
"""

from io import StringIO
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe
from mutopia.models import Composer, License, Style, Instrument

@require_safe
def db_hook(request):
    """A request to provide a minimal JSON description of the database.

    :param request: HTTPRequest object
    :returns: response object with JSON content
    :rtype: JsonResponse

    """

    dbdict = {'instruments': [],
              'composers': [],
              'styles': [],
              'licenses': [],
    }
    for instrument in Instrument.objects.all():
        dbdict['instruments'].append(instrument.instrument)

    for composer in Composer.objects.all():
        dbdict['composers'].append(composer.composer)

    for style in Style.objects.all():
        dbdict['styles'].append(style.style)

    for license_obj in License.objects.all():
        dbdict['licenses'].append(license_obj.name)

    return JsonResponse(dbdict)
