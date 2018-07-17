# apps/social_media/urls.py

from django.conf.urls import url
from . import views
from views import DashboardListView, MyAlbumListView, ViewPostDetailView

app_name = 'social_media'
urlpatterns = [
    url(r'^$', DashboardListView.as_view(), name='index'),

    url(r'^myAccount$', views.myAccount, name='myAccount'),

    url(r'^myAlbum/(?P<id>\d+)$', MyAlbumListView.as_view(), name='myAlbum'),

    url(r'^viewPost/(?P<pk>\d+)$', ViewPostDetailView.as_view(), name='viewPost'),

    url(r'^new_post$', views.new_post, name='new_post'),
    url(r'^new_comment/(?P<id>\d+)$', views.new_comment, name='new_comment'),
    url(r'^delete_post/(?P<id>\d+)$', views.delete_post, name='delete_post'),
    # url(r'^new_comment$', views.new_comment, name='new_comment'),
]
