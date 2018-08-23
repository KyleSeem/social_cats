# -*- coding: utf-8 -*-
# apps/social_media/models.py

from __future__ import unicode_literals, print_function
import os, sys

from PIL import Image, ImageFile
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile




# define variables for desired date and time formats for save path structure
upload_date_time = str(datetime.now())
dt = upload_date_time.split(' ', 1)
time = dt[1].split('.', 1)

# save path for uploaded images
def upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<YYYY-MM-DD>/<filename>_<hhmmss>
    return 'user_{0}/{1}/{2}_{3}'.format(instance.user.id, dt[0], time[0], filename)


# save path for users' profile picture
def avatar_upload_path(instance, filename):
    # save to user's media folder in avatar subfolder - should only ever be one image saved here
    return 'user_{0}/avatar/{1}_{2}'.format(instance.user.id, time[0], filename)


# user's additional personal details (all optional)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=55, blank=True)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'user profile'


    def display_user_id(self):
        return self.user.id
    display_user_id.short_description = "User ID"

    def display_bio(self):
        # creating short string for admin site display
        return self.bio[:20] + '...'
    display_bio.short_description = "Bio"

    # reset avatar to default
    def set_avatar_to_default(self):
        default = 'media/default_avatar/avatar.jpg'
        d = open(default)
        copyFile = ContentFile(d.read())
        newName = default.split("/")[-1]
        newDefault = self.avatar.save(newName, copyFile)
        return self.avatar



# create profile object and set default avatar when new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.set_avatar_to_default()


# save user profile any time the user model is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# whole post - includes user, photo and user-added caption
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=upload_path)
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('viewPost', args=[str(self.id)])

    def __str__(self):
        return str(self.id)




# comments are tied to a single post, include commentor as user and post id
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return str(self.id)



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return str(self.id)


####
