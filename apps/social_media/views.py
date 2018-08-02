# -*- coding: utf-8 -*-
# apps/social_media/views.py

from __future__ import unicode_literals
import os

from django.template import RequestContext

from django.views.generic import ListView, DetailView, UpdateView

from PIL import Image
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from urlparse import urlparse
from os.path import splitext, basename
from .models import User, Photo, Post, Comment, Profile, Avatar
from .forms import PhotoUploadForm, NewPostForm, NewCommentForm, AvatarForm


# session info: userID is id of logged in user, thisUser is username of logged in user

###### NAVIGATION ######

# DASHBOARD - landing page
class DashboardListView(ListView):
    model = Post
    template_name = 'social_media/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
    # define context for dashboard
        context = super(DashboardListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['photos'] = Photo.objects.all()
        context['comments'] = Comment.objects.all()
        context['nav_dashboard'] = 'active'

        return context


# MYALBUM - user's album page
class MyAlbumListView(ListView):
    model = Post
    template_name = 'social_media/album.html'
    context_object_name = 'thisUser'

    def get_queryset(self):
        return Post.objects.all()

        # write alternate if decide to use guest login options

    def get_context_data(self, *args, **kwargs):
        id = self.kwargs['id']
    # define context for user's album
        context = super(MyAlbumListView, self).get_context_data(**kwargs)
        context['thisUser'] = User.objects.get(id=id)
        context['posts'] = Post.objects.filter(user=id).order_by('-created_at')
        context['photos'] = Photo.objects.filter(user=id)
        context['comments'] = Comment.objects.all()
        context['users'] = User.objects.all()
        context['nav_myAlbum'] = 'active'

        return context


class ViewPostDetailView(DetailView):
    model = Post
    template_name = 'social_media/view_post.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        id = self.kwargs['pk']

        context = super(ViewPostDetailView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=id)
        context['comments'] = Comment.objects.filter(post=id).order_by('-created_at')
        context['users'] = User.objects.all()

        return context


# MYACCOUNT - user's acount page
class MyAccountListView(ListView):
    model = User
    template_name = 'social_media/account.html'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        id = self.kwargs['pk']

        context = super(MyAccountListView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=id)
        context['avatar'] = Avatar.objects.get(user=id)
        context['form'] = AvatarForm()

        return context



###### CRUD ######


# create and save new photo and new post objects
def new_post(request):
    if request.method == "POST":
        photo_form = PhotoUploadForm(request.POST, request.FILES)
        post_form = NewPostForm(request.POST)

        # if BOTH forms pass validation
        if all([photo_form.is_valid(), post_form.is_valid()]):
            # save new photo object
            new_photo = photo_form.save()
            # save new post (uses default as placeholder for photo field)
            new_post = post_form.save()
            # get new_post object and update photo field with new_photo object
            new_post.photo = Photo.objects.get(id=new_photo.id)
            # save changes to new_post object
            new_post.save()

            return redirect(reverse('social_media:index'))

        else:
            # 404 error page with reroute link or something like that
            return HttpResponse('INVALID FORM')


# create and save new comment for specified post
def new_comment(request, id):
    if request.method == "POST":
        print ('-'*40)
        # id = id
        post = Post.objects.get(id=request.POST['post'])
        form = NewCommentForm(request.POST)

        # save new comment and update post's comment count
        if form.is_valid():
            comment = form.save()
            post.com_count += 1
            post.save()
            return redirect(reverse('social_media:viewPost', kwargs={'pk':post.id}))
        else:
            ########### make some error
            print ('invalid comment')
            print form.errors
            return redirect(reverse('social_media:index'))


# delete post and all associated objects (comments, photo)
def delete_post(request, id):
    if request.method == "POST":
        user_id = request.POST['user']
        photo = Photo.objects.get(id=request.POST['photo'])

        # delete photo object from photo model - this will remove file from media folder (uses django_cleanup)
        # post object will delete on cascade
        photo.delete()

        # upon successful delete, get the previous path and return user to it (album or dashboard)
        previous_page = urlparse(request.POST['previous'])

        if previous_page.path == ('/kittenstagram/myAlbum/' +user_id):
            # return user to their album page
            return redirect(reverse('social_media:myAlbum', kwargs={'id':user_id}))
        else:
            # return user to the dashboard
            return redirect(reverse('social_media:index'))


# set profile picture/avatar
def set_avatar(request):

    id = request.session['sessionUserID']
    if request.method == "POST":
        print ('-'*40)
        print ('session user id', id)

        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            print 'valid'
            form.save()
            return redirect(reverse('social_media:myAccount', kwargs={'pk':id}))
        else:
            print 'NOT VALID!!!'
            return redirect(reverse('social_media:myAccount', kwargs={'pk':id}))
    else:
        form = AvatarForm()
    return redirect(reverse('social_media:myAccount', kwargs={'id':id}))




###### ERRORS ######
def handler404(request):
    response = render_to_response('404.html', {},
        context_instance=RequestContext(request))
    response.status_code = 404
    return response


#####
