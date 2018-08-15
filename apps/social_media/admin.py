from django.contrib import admin
from .models import Profile, Post, Comment
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('display_user_id', 'user', 'nickname', 'location', 'dob', 'display_bio', 'avatar')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'caption', 'com_count', 'likes')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment')
