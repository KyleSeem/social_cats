# apps/social_media/forms.py

from PIL import Image
from django import forms
from django.core.files import File
from .models import User, Photo, Post, Comment, Avatar, Profile


class PhotoUploadForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        # fields = ('user', 'photo')
        fields = ('user', 'photo', 'x', 'y', 'width', 'height',)



class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'caption',)


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
        model = Avatar
        fields = ('user', 'file', 'x', 'y', 'width', 'height',)







######
