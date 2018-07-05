# -*- coding: utf-8 -*-
# apps/social_media/views.py

from __future__ import unicode_literals
import os

from django.views.generic import ListView, DetailView, UpdateView

from PIL import Image
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import JsonResponse
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

class DashboardDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(DashboardDetail, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['photos'] = Photo.objects.all()
        context['comments'] = Comment.objects.all()
        context['nav_dashboard'] = 'active'
        return context




class ViewPostListView(ListView):
    template_name = 'social_media/view_modal.html'
    context_object_name = 'this_post'

    def get_post(request):
        print ('-'*40)
        print self
        print ('-'*40)





def get_post(request):

    print ('-'*40)
    print id
    print ('-'*40)



###### NAVIGATION ######


# user's album
def myAlbum(request):
    context = {
        'myPhotos':Photo.objects.filter(user=request.session['sessionUserID']),
        'nav_myAlbum':'active',
        'launch':0
    }
    if request.method == "GET":
        print ('-'*20)
        return render(request, 'social_media/album.html', context)



# user's acount page
def myAccount(request, **kwargs):
    ##### add validation to show only user's info OR change to id kwarg

    context = {
        'users':User.objects.all(),
        'nav_account':'active',
    }
    return render(request, 'social_media/account.html', context)


# view modal
def view_post(request):
    # called on modal close - removes session that tells jquery to launch modal
    if request.method == "GET":
        del request.session['this_post']
        return redirect(reverse('social_media:index'))

    # called when post is clicked - creates session data that tells jquery to launch modal
    if request.method == "POST":
        request.session['this_post'] = request.POST['this_post']
        return redirect(reverse('social_media:index'))



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


# delete photo - if user 'cancels' out of modal instead of submitting new post, delete the canceled photo from database
def scrap(request):
    if request.method == "POST":
        photo = Photo.objects.get(id=request.session['pID'])
        photo.delete()
        request.session['pID'] = 0
        return redirect(reverse('social_media:index'))


# create new post - takes image that was just saved and combines with user input
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save()
            request.session['pID'] = 0
            return redirect(reverse('social_media:index'))
        else:
            print ('invalid post')
            print form.errors
            return redirect(reverse('social_media:index'))


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
