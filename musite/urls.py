"""musite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/

"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import handler404
from mutopia import views, piece_views
from mutopia.rss import LatestEntriesFeed, AtomLatestFeed
from mutopia import hooks

urlpatterns = [
    url(r'^$',
        views.homepage,
        name='home'),
    url(r'^browse/',
        views.browse,
        name='browse'),
    url(r'^search/',
        views.adv_search,
        name='search'),
    url(r'^legal/',
        views.legal,
        name='legal'),
    url(r'^contribute/',
        views.contribute,
        name='contribute'),
    url(r'^contact/',
        views.contact,
        name='contact'),
    url(r'^piece/', include('mutopia.urls')),
    url(r'key-results/',
        views.key_results,
        name='key-results'),
    url(r'adv-results/',
        views.adv_results,
        name='adv-results'),
    url(r'^admin/', admin.site.urls),
    url(r'latest/rss/$',
        LatestEntriesFeed(),
        name='latest-rss'),
    url(r'latest/atom/$',
        AtomLatestFeed(),
        name='latest-atom'),
    url(r'github/', include('github.urls')),
    url(r'update/', include('update.urls')),
    url(r'db_hook/', hooks.db_hook),
]

handler404 = 'mutopia.views.handler404'
