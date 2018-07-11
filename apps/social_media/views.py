# -*- coding: utf-8 -*-
# apps/social_media/views.py

from __future__ import unicode_literals
import os

from django.views.generic import ListView, DetailView, UpdateView

from PIL import Image
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from .models import User, Photo, Post, Comment
from .forms import PhotoUploadForm, NewPostForm, NewCommentForm


# session info: userID is id of logged in user, thisUser is username of logged in user

# dashboard/main page
class DashboardListView(ListView):
    model = Post
    template_name = 'social_media/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(DashboardListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['photos'] = Photo.objects.all()
        context['comments'] = Comment.objects.all()
        context['nav_dashboard'] = 'active'
        return context

# user's album page
class MyAlbumListView(ListView):
    model = Post
    template_name = 'social_media/album.html'
    context_object_name = 'thisUser'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

        # write alternate if decide to use guest login options

    def get_context_data(self, *args, **kwargs):
        # print ('-'*40)
        id = self.kwargs['id']

        context = super(MyAlbumListView, self).get_context_data(**kwargs)
        context['thisUser'] = User.objects.get(id=id)
        context['posts'] = Post.objects.filter(user=id)
        context['photos'] = Photo.objects.filter(user=id)
        context['comments'] = Comment.objects.all()
        context['users'] = User.objects.all()
        context['nav_myAlbum'] = 'active'
        return context



def deletePost(request):
    if request.method == "POST":
        print ('-'*40)




###### NAVIGATION ######




# user's acount page
def myAccount(request, **kwargs):
    ##### add validation to show only user's info OR change to id kwarg

    context = {
        'users':User.objects.all(),
        'nav_account':'active',
    }
    return render(request, 'social_media/account.html', context)





###### CRUD ######

# create photo - from image upload, validate and save
def add_photo(request):
    ####### use alerts array or messages????
    # alerts = []
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            im = Image.open(request.FILES['photo'])
            if im.size[0] >= im.size[1]:
                orientation = 'ls'
            else:
                orientation = 'pt'

            new_photo = form.save()

            new_photo.orientation = orientation
            new_photo.save()

            request.session['pID'] = new_photo.id
            return redirect(reverse('social_media:index'))

        else:
            print ('invalid entry')
            return redirect(reverse('social_media:index'))



# create new post - takes image that was just saved and combines with user input
# def new_post(request):
#     if request.method == "POST":
#         form = NewPostForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             return redirect(reverse('social_media:index'))
#         else:
#             print ('invalid post')
#             print form.errors
#             return redirect(reverse('social_media:index'))



def new_post(request):
    if request.method == "POST":
        photo_form = PhotoUploadForm(request.POST, request.FILES)

        if photo_form.is_valid():
            new_photo = photo_form.save()
            print ('-'*40)
            print (new_photo.id, new_photo.user, new_photo.photo, new_photo.orientation)
            print ('-'*40)

        ######

            post_form = NewPostForm(request.POST)
            if post_form.is_valid():
                print ('POST FORM VALID')
                new_post = post_form.save()
                print ('%'*20)
                print (new_post.id, new_post.photo.id, new_post.user.id, new_post.caption)
                print ('%'*20)

                return redirect(reverse('social_media:index'))
            else:
                return HttpResponse('INVALID POST FORM')

        else:
            return HttpResponse('INVALID PHOTO FORM')



        # return HttpResponse('returned')


def new_comment(request):
    if request.method == "POST":
        print request.POST
        form = NewCommentForm(request.POST)
        if form.is_valid():
            print ('valid comment')
            comment = form.save()
            return redirect(reverse('social_media:index'))
        else:
            print ('invalid comment')
            print form.errors
            return redirect(reverse('social_media:index'))
