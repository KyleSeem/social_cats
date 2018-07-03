from django.conf.urls import url
from . import views

app_name = 'login_reg'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
]
