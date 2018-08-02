# apps/social_media/forms.py

from PIL import Image
from django import forms
from django.core.files import File
from .models import User, Photo, Post, Comment, Avatar, Profile


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('user', 'photo', 'orientation')
        # error_messages = {
        #     'invalid': 'Invalid file format: selection must be image file type'
        # }


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'caption')


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

        def save(self):
            avatar = super(AvatarForm, self).save()

            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(avatar.file)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(avatar.file.path)
            print ('-'*40)
            print avatar.file.path

            return avatar






######
