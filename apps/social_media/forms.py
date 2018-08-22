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
        # model = Avatar
        # fields = ('user', 'file', 'x', 'y', 'width', 'height',)

        model = Profile
        fields = ('avatar', 'x', 'y', 'width', 'height',)


class UpdateBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'location',)


######
