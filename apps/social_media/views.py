# -*- coding: utf-8 -*-
# apps/social_media/views.py

from __future__ import unicode_literals
import os

from django.template import RequestContext

from django.views import generic
from django.views.generic import ListView, DetailView, UpdateView

from PIL import Image
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from urlparse import urlparse
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Profile
from .forms import NewPostForm, NewCommentForm, AvatarForm, RegisterForm



# NOTE: class-based views get method_decorator for authentication, other views get login_required decorator

###### NAVIGATION ######

# DASHBOARD - landing page
@login_required
def index(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()
    newPostForm = NewPostForm()
    user = request.user


    context = {
        'user': user,
        'users': users,
        'profiles': profiles,
        'posts': posts,
        'comments': comments,
        'newPostForm': newPostForm,
        'nav_dashboard': 'active',
    }

    return render(request, 'social_media/index.html', context=context)



# MYALBUM - user's album page
@method_decorator(login_required, name='dispatch')
class MyAlbumListView(generic.ListView):
    model = User
    template_name = 'social_media/album.html'

    def get_context_data(self, **kwargs):
        id = self.kwargs['id']
        context = super(MyAlbumListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=id)
        context['nav_myAlbum'] = 'active'


        return context



# MYACCOUNT - user's acount page
@method_decorator(login_required, name='dispatch')
class MyAccountListView(generic.ListView):
    model = User
    template_name = 'social_media/account.html'

    def get_context_data(self, **kwargs):
        id = self.kwargs['id']
        context = super(MyAccountListView, self).get_context_data(**kwargs)
        context['form'] = AvatarForm()

        return context


# VIEW POST - view selected post
@method_decorator(login_required, name='dispatch')
class ViewPostDetailView(generic.DetailView):
    model = Post
    template_name = 'social_media/view_post.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        id = self.kwargs['pk']
        context = super(ViewPostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=id)

        return context




###### OTHER CRUD ######
# REGISTER - create new user
def register(request):
    if request.method == "POST":
        request.session['reg_username'] = request.POST['username']
        request.session['reg_email'] = request.POST['email']

        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password= raw_password)
            login(request, user)
            del request.session['reg_username']
            del request.session['reg_email']

            return redirect('social_media:index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form':form})



# NEW POST - create and save new photo and new post objects
@login_required
def new_post(request):
    if request.method == "POST":

        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            photo = form.cleaned_data.get('photo')

        # save new post object
            new_post = form.save()

        # open image file to adjust cropped proportions
            image = Image.open(new_post.photo)
            cropped_image = image.crop((x, y, w+x, h+y))

        # determine photo orientation and resize accordingly (landscape, portrait, square)
            if w > h:
                resized_image = cropped_image.resize((600, 450), Image.ANTIALIAS)
            elif w < h:
                resized_image = cropped_image.resize((450, 600), Image.ANTIALIAS)
            elif w == h:
                resized_image = cropped_image.resize((450, 450), Image.ANTIALIAS)

        # save resized image file
            resized_image.save(new_post.photo.path)
            return redirect(reverse('social_media:index'))

    else:
        return redirect(reverse('social_media:index'))


# NEW COMMENT - create and save new comment for specified post
@login_required
def new_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)

        if form.is_valid():
            comment = form.save()
            post.com_count += 1
            post.save()

    return redirect(reverse('social_media:viewPost', kwargs={'pk':id}))



# DELETE POST and all associated objects (comments, photo)
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if request.user.id == post.user.id:
            post.delete()
            return redirect(reverse('social_media:myAlbum', kwargs={'id':request.user.id}))

    else:
        return redirect(reverse('social_media:viewPost', kwargs={'pk':pk}))


# DELETE COMMENT - delete comment from user post
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.id)

    if request.method == "POST":
        if request.user.id == comment.user.id:
            comment.delete()

    return redirect(reverse('social_media:viewPost', kwargs={'pk':post.id}))


# AVATAR - set profile picture/avatar
@login_required
def set_avatar(request, id):
    print request.user.profile.avatar
    if request.method == "POST":
        # set form to target the profile associated with this user
        form = AvatarForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            print "VALID"
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            avatar = form.cleaned_data.get('avatar')


            # profile = form.save()
            #
            # image = Image.open(profile.avatar)
            # cropped_image = image.crop((x, y, w+x, h+y))
            # resized_image = cropped_image.resize((450, 450), Image.ANTIALIAS)
            # resized_image.save(profile.avatar.path)

            return redirect(reverse('social_media:myAccount', kwargs={'id':id}))
        else:
            print 'NOT VALID!!!'
        ######## ADD ERROR MESSAGE AND RETURN ######
            # should there be a backup function that resets the avatar to default if error or if null?
            # return redirect(reverse('social_media:myAccount', kwargs={'id':id}))
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
