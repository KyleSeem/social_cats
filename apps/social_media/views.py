# -*- coding: utf-8 -*-
# apps/social_media/views.py

from __future__ import unicode_literals
import os

from django.template import RequestContext

from django.views import generic
from django.views.generic import ListView, DetailView, UpdateView

from PIL import Image
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .middleware import get_current_user
from django.contrib.auth.models import User
from .models import Post, Comment, Profile, Like
from .forms import RegisterForm, NewPostForm, NewCommentForm, AvatarForm, UpdateBioForm, UpdateUserModelForm, UpdateProfileForm



# NOTE: class-based views get method_decorator for authentication, other views get login_required decorator

# def set_timezone(request):
#     if request.method == "POST":
#         request.session['django_timezone'] = request.POST['timezone']


###### NAVIGATION ######

# DASHBOARD - landing page - initial data grab to pass to generic views
@login_required
def index(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()
    newPostForm = NewPostForm()

    # compile array of posts that current user has liked so hearts appear correctly
    like_array = []
    for l in Like.objects.filter(user=request.user):
        like_array.append(l.post.id)

    # now = timezone.localtime(timezone.now())
    # print now


    context = {
        # 'now':now,
        'users': users,
        'profiles': profiles,
        'posts': posts,
        'comments': comments,
        'like_array': like_array,
        'newPostForm': newPostForm,
        'nav_dashboard': 'active',
        'btn_display': 'd-none',
    }
    return render(request, 'social_media/index.html', context=context)



# MYALBUM - user's album page
@method_decorator(login_required, name='dispatch')
class MyAlbumListView(generic.ListView):
    model = User
    template_name = 'social_media/album.html'

    def get_context_data(self, **kwargs):
        id = self.kwargs['id']
        # determine nav_bar active status: current user = active
        a = get_current_user()
        b = int(id)
        if a == b:
            nav_status = 'active'
            other_status = ''
        else:
            nav_status = ''
            other_status = 'active'

        context = super(MyAlbumListView, self).get_context_data(**kwargs)
        context['album_owner'] = User.objects.get(id=id)
        context['posts'] = Post.objects.filter(user=id)
        context['nav_myAlbum'] = nav_status
        context['other_album'] = other_status

        return context



# MYACCOUNT - user's acount page
@method_decorator(login_required, name='dispatch')
class MyAccountListView(generic.ListView):
    model = User
    template_name = 'social_media/account.html'

    def get_context_data(self):
        id = get_current_user()
        context = super(MyAccountListView, self).get_context_data()
        context['form'] = AvatarForm()
        context['nav_myAccount'] = 'active'

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
        user_id = get_current_user()
        like_array = []
        for l in Like.objects.filter(user=user_id):
            like_array.append(l.post.id)

        context = super(ViewPostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=id)
        context['like_array'] = like_array

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


# DELETE ACCOUNT - delete user's account
@login_required
def delete_account(request):
    if request.method == "POST":
        # check the password entered against the current user's password
        user = authenticate(username=request.user.username, password=request.POST['password'])

        if user is not None:
            # if the password matches the current user's password (is_authenticated)
            User.objects.get(id=request.user.id).delete()
            return redirect('social_media:register')
        else:
            error = "Password does not match our records."
            return render(request, 'social_media/delete_account.html', {'error':error})

    else:
        return render(request, 'social_media/delete_account.html')





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
            error_message = "You have selected an invalid file type."
            return my_error_handler(request, error_message)
    else:
        return redirect(reverse('social_media:index'))


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



# NEW COMMENT - create and save new comment for specified post
@login_required
def new_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)

        if form.is_valid():
            comment = form.save()
            post.save()

    return redirect(reverse('social_media:viewPost', kwargs={'pk':id}))


# DELETE COMMENT - delete comment from user post
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.id)

    if request.method == "POST":
        if request.user.id == comment.user.id:
            comment.delete()

    return redirect(reverse('social_media:viewPost', kwargs={'pk':post.id}))



# LIKE OR UNLIKE POST
@login_required
def toggle_like(request):
    status = 'created'
    post = Post.objects.get(id=request.GET.get('post_id', None))

    like, created = Like.objects.filter(
        Q(post=post) | Q(user=request.user),
    ).get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        status = 'deleted'

    data = {
        'status': status
    }
    return JsonResponse(data)



# SET AVATAR - set profile picture/avatar
@login_required
def set_avatar(request):
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

            profile = form.save()

            image = Image.open(profile.avatar)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((450, 450), Image.ANTIALIAS)
            resized_image.save(profile.avatar.path)

            return redirect(reverse('social_media:myAccount'))
        else:
            print 'NOT VALID!!!'
        ######## ADD ERROR MESSAGE AND RETURN ######
    else:
        form = AvatarForm()
    # return redirect(reverse('social_media:myAccount'))
    return render(request, 'social_media/account.html', { 'form': form })


# DELETE AVATAR - delete existing avatar - will force re-creation of default as avatar
@login_required
def delete_avatar(request):
    profile = Profile.objects.get(user=request.user.id)
    profile.set_avatar_to_default()

    return redirect(reverse('social_media:myAccount'))


# UPDATE PROFILE (and/or User model)
@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UpdateUserModelForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # form errors are displayed in page
    else:
        user_form = UpdateUserModelForm()
        profile_form = UpdateProfileForm()
    return render(request, 'social_media/account.html', { 'user_form': user_form, 'profile_form': profile_form })


# UPDATE BIO (profile model)
@login_required
def update_bio(request):
    if request.method == "POST":

        bio_form = UpdateBioForm(request.POST, instance=request.user.profile)
        if bio_form.is_valid():
            bio_form.save()

            # form errors are displayed in page
    else:
        bio_form = UpdateBioForm(instance=request.user.profile)
    return render(request, 'social_media/account.html', { 'bio_form': bio_form })


###### ERRORS ######
def my_error_handler(request, error_message):
    print error_message
    return render(request, 'social_media/error.html', {'error_message': error_message})


#####
