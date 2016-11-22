from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^push_hook/$', views.push_hook),
]
