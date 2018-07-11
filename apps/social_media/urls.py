# apps/social_media/urls.py

from django.conf.urls import url
from . import views
from views import DashboardListView, MyAlbumListView

app_name = 'social_media'
urlpatterns = [
    url(r'^$', DashboardListView.as_view(), name='index'),

    url(r'^myAccount$', views.myAccount, name='myAccount'),

    url(r'^myAlbum/(?P<id>\d+)$', MyAlbumListView.as_view(), name='myAlbum'),

    url(r'^add_photo$', views.add_photo, name='add_photo'),
    url(r'^new_post$', views.new_post, name='new_post'),
    url(r'^new_comment$', views.new_comment, name='new_comment'),
    # url(r'^scrap$', views.scrap, name='scrap'),
]
