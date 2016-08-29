from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^status/$', views.site_status, name='site-status'),
]
