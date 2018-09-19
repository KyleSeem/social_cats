# apps/kyleseem/urls.py

from django.conf.urls import url
from . import views

app_name = 'kyleseem'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
