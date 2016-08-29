from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_safe
from mutopia.models import Piece

@require_safe
def site_status(request):
    """A request to view the status of the site.

    Return various bits of information about a site in a JSON object.
    The following example retrieves the last mutopia piece id, ::

      import requests
      r = requests.head('http://<site>/status/')
      incoming = json.loads(r.content.decode('utf-8'))
      print(incoming['LastID'])

    :param request: HTTPRequest object
    :returns: response object with json content
    :rtype: JsonResponse

    """

    piecemax = Piece.objects.all().aggregate(Max('piece_id'))
    next_id = int(piecemax['piece_id__max']) + 1
    response = JsonResponse({'LastID': piecemax['piece_id__max']})
    return response
