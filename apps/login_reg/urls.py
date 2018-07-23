# apps/login_reg/urls.py

from django.conf.urls import url
from . import views

app_name = 'login_reg'
urlpatterns = [
    url(r'^$', views.user_login),
    url(r'^user_login$', views.user_login, name='user_login'),
    url(r'^reg_form$', views.reg_form, name='reg_form'),
    url(r'^guest$', views.guest, name='guest'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
]
