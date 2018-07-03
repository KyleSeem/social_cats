# apps/social_media/forms.py

from django import forms
from .models import User, Photo, Post, Comment


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('user', 'photo')
        # error_messages = {
        #     'invalid': 'Invalid file format: selection must be image file type'
        # }


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'photo', 'caption')


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'comment')
