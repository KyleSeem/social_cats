# apps/social_media/forms.py

from PIL import Image
from django import forms
from django.core.files import File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile, Like


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=60, error_messages={
        'invalid': 'Username may only contain English letters, numbers, and @/./+/-/_ characters.',
        'unique': 'Username already exists.'
    })
    email = forms.EmailField(max_length=254, help_text='Required', error_messages={'unique': 'Email has already been registered.'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # require unique email address
    User._meta.get_field('email')._unique=True


class NewPostForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = ('user', 'photo', 'x', 'y', 'width', 'height', 'caption',)


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'comment')


class AvatarForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('avatar', 'x', 'y', 'width', 'height',)


class UpdateBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)


class UpdateUserModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, error_messages={
        'max_length': "First name may not exceed 30 characters in length.",
    })
    last_name = forms.CharField(max_length=30, required=False, error_messages={
        'max_length': "Last name may not exceed 30 characters in length.",
    })
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)



class UpdateProfileForm(forms.ModelForm):
    nickname = forms.CharField(max_length=60, required=False, error_messages={
        'max_length': "Nickname may not exceed 60 characters in length.",
    })
    location = forms.CharField(max_length=75, required=False, error_messages={
        'max_length': "Location may not exceed 75 characters, which should be plenty... even if you live in Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch, Anglesey, Wales.",
    })
    class Meta:
        model = Profile
        fields = ('nickname', 'location',)


######
