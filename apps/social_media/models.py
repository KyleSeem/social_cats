# -*- coding: utf-8 -*-
# apps/social_media/models.py

from __future__ import unicode_literals, print_function
import os, sys

from PIL import Image, ImageFile
from datetime import datetime
from django.db import models
from ..login_reg.models import User


# save path for uploaded images
def upload_path(instance, filename):
    # define variables for desired date and time formats for save path structure
    upload_date_time = str(datetime.now())
    dt = upload_date_time.split(' ', 1)
    time = dt[1].split('.', 1)

    # file will be uploaded to MEDIA_ROOT/user_<id>/<YYYY-MM-DD>/<filename>_<hhmmss>
    return 'user_{0}/{1}/{2}_{3}'.format(instance.user.id, dt[0], filename, time[0])




# just the uploaded image with user connection
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=upload_path)
    orientation = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'photos'


# whole post - includes user, photo and user-added caption
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, default=1)
    caption = models.CharField(max_length=255)
    com_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'

# comments are tied to a single post, include commentor as user and post id
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
