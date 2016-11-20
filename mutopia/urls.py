from django.conf.urls import url
from . import piece_views

urlpatterns = [
    url(r'^info/(?P<piece_id>[0-9]+)/$',
        piece_views.piece_info,
        name='piece-info'),
    url(r'^log/(?P<piece_id>[0-9]+)/$',
        piece_views.log_info,
        name='piece-log'),
    url(r'^latest_additions/',
        piece_views.latest_additions,
        name='latest_additions'),
    url(r'^instrument/(?P<instrument>[\w]+)/$',
        piece_views.piece_by_instrument,
        name='piece-by-instrument'),
    url(r'^style/(?P<slug>[\-\w]+)/$',
        piece_views.piece_by_style,
        name='piece-by-style'),
    url(r'^composer/(?P<composer>[\-\w]+)/$',
        piece_views.piece_by_composer,
        name='piece-by-composer'),
    url(r'^collection/(?P<col_tag>[\w]+)/$',
        piece_views.collection_list,
        name='collection-list'),
    url(r'^version/(?P<version>[0-9A-Za-z\.]+)/$',
        piece_views.piece_by_version,
        name='piece-by-version'),
]
