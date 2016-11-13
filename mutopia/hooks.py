"""GITHUB hooks (webhooks)
This is a template. If hooks aren't used, this can be removed.
"""

from io import StringIO
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Note that we need csrf_exempt here because the request will not come
# from a django form.

@csrf_exempt
def push_hook(request):
    """A push-hook template.

    Add the URL pointing to this method as a GITHUB webhook. String
    content in the response object can be viewed in the webhook log.

    :param request: defines protocol for adding method to urls.py
    :returns: An HttpResponse object.

    """
    # make sure our expections are met
    if request.content_type != 'application/json':
        return HttpResponse('Content is not JSON')
    if request.method != 'POST':
        return HttpResponse('Hook got a non-POST event, ignored.')

    jbody = json.loads(request.body.decode('utf-8'))
    jbuffer = StringIO()
    jbuffer.write('pusher is: ' + jbody['pusher']['name'])
    jbuffer.write('Commits:\n')
    for commit in jbody['commits']:
        for modified in commit['modified']:
            jbuffer.write(' Modified: '+modified)
            jbuffer.write('\n')
        for removal in commit['removed']:
            jbuffer.write(' Removed: '+removal)
            jbuffer.write('\n')
        for addition in commit['added']:
            jbuffer.write(' Added: '+addition)
            jbuffer.write('\n')
    # anything else ?
    return HttpResponse(buf.getvalue())
