# apps/social_media/urls.py

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from views import MyAlbumListView, ViewPostDetailView, MyAccountListView

app_name = 'social_media'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^myAccount/$', views.MyAccountListView.as_view(), name='myAccount'),
    url(r'^myAlbum/(?P<id>\d+)$', views.MyAlbumListView.as_view(), name='myAlbum'),
    url(r'^viewPost/(?P<pk>\d+)$', views.ViewPostDetailView.as_view(), name='viewPost'),
    url(r'^about/$', views.about, name='about'),

    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^delete_post/(?P<pk>\d+)$', views.delete_post, name='delete_post'),

    url(r'^new_comment/(?P<id>\d+)$', views.new_comment, name='new_comment'),
    url(r'^delete_comment/(?P<pk>\d+)$', views.delete_comment, name='delete_comment'),

    url(r'^set_avatar/$', views.set_avatar, name='set_avatar'),
    url(r'^delete_avatar/$', views.delete_avatar, name='delete_avatar'),

    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^update_bio/$', views.update_bio, name='update_bio'),

    url(r'^delete_account/$', views.delete_account, name='delete_account'),

    # ajax urls
    url(r'^ajax/toggle_like/$', views.toggle_like, name='toggle_like'),
    url(r'^ajax/set_user_timezone/$', views.set_user_timezone, name='set_user_timezone'),

    # authentication urls
    url(r'^login/$', auth_views.login, {'template_name':'registration/login.html'}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^guest_login/$', views.guest_login, name='guest_login'),
]
