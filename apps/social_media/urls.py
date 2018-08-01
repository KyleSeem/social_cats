# apps/social_media/urls.py

from django.conf.urls import url
from . import views
from views import DashboardListView, MyAlbumListView, ViewPostDetailView, MyAccountListView

app_name = 'social_media'
handler404 = 'social_media.views.handler404'

urlpatterns = [
    url(r'^dashboard$', DashboardListView.as_view(), name='index'),

    url(r'^myAccount/(?P<pk>\d+)$', MyAccountListView.as_view(), name='myAccount'),
    # url(r'^myAccount$', views.myAccount, name='myAccount'),

    url(r'^myAlbum/(?P<id>\d+)$', MyAlbumListView.as_view(), name='myAlbum'),

    url(r'^viewPost/(?P<pk>\d+)$', ViewPostDetailView.as_view(), name='viewPost'),

    url(r'^new_post$', views.new_post, name='new_post'),
    url(r'^new_comment/(?P<id>\d+)$', views.new_comment, name='new_comment'),
    url(r'^delete_post/(?P<id>\d+)$', views.delete_post, name='delete_post'),
    url(r'^set_profile_pic$', views.set_profile_pic, name='set_profile_pic'),
]
