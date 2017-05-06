from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import StringIO
import json
from mutopia.models import AssetMap


def _get_asset_info(infile):
    if not infile.startswith('ftp/'):
        return None
    fvec = []
    has_lys = False
    for part in infile.split('/')[1:]:
        if part.endswith('-lys'):
            has_lys = True
            break
        if part.endswith('.ly'):
            break
        if part.endswith('.ily'):
            break
        fvec.append(part)
    return ('/'.join(fvec), has_lys)


_IGNORES = {'Makefile', '.gitignore'}


# Note that we need csrf_exempt here because the request will not come
# from a django form.

@csrf_exempt
def push_hook(request):
    """A github push hook for recording pending site updates.

    This is a django view targeted to respond to be "hooked" to a
    github repository push command. When a push arrives, the
    appropriate ``AssetMap`` entity is found (or created) and is
    marked for update.

    :param request: defines protocol for adding method to urls.py
    :returns: An HttpResponse object.

    The hook is assigned in the sites github repository,

      - Select `Setting`
      - Select `Webhooks`
      - Select `Add webhook`
      - Add the url of this hook as the `Payload`, i.e.,
        `<site-url>/github/push_hook`.
      - Change `Content type` to `application/json`
      - The only event needed is the `push event`

    String content in the response object can be viewed in the webhook
    log.

    """
    # make sure our expections are met
    if request.content_type != 'application/json':
        return HttpResponse('Content is not JSON')
    if request.method != 'POST':
        return HttpResponse('Hook got a non-POST event, ignored.')

    jbody = json.loads(request.body.decode('utf-8'))
    jbuffer = StringIO()
    if 'pusher' in jbody:
        jbuffer.write('Processing push by: {0}\n'.format(jbody['pusher']['name']))
    if 'commits' in jbody:
        asset_dict = dict()
        for commit in jbody['commits']:
            for modified in commit['modified']:
                asset_info = _get_asset_info(modified)
                if asset_info:
                    asset_dict[asset_info[0]] = asset_info[1]
            for addition in commit['added']:
                asset_info = _get_asset_info(addition)
                if asset_info:
                    asset_dict[asset_info[0]] = asset_info[1]
        # Iterate dictionary items to update/create the associated asset.
        for folder,has_lys in asset_dict.items():
            name = folder[folder.rfind('/')+1:]
            try:
                asset = AssetMap.objects.get(folder=folder)
                asset.has_lys = has_lys
                asset.name = name
                # mark unpublished to force subsequent update to
                # reread the RDF file.
                asset.published = False
                asset.save()
                jbuffer.write('[update] - ')
            except AssetMap.DoesNotExist:
                # Create the new asset.
                # No piece_id is assigned at this time but it could
                # be.
                if name in _IGNORES:
                    folder = folder + ' (ignored)'
                    continue
                asset = AssetMap.objects.create(folder=folder,
                                                name=name,
                                                has_lys=has_lys)
                asset.save()
                jbuffer.write('[new]    - ')
            jbuffer.write(folder)
            jbuffer.write('\n')
    else:
        jbuffer.write('No commits to process.\n')

    return HttpResponse(jbuffer.getvalue())
