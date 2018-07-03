# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def login(self, postData):
        email = postData['log_email']
        password = postData['password']

        alerts = []

        if len(email) < 1:
            alerts.append('Please enter email address')

        try:
            user = User.objects.get(email=email)
        except:
            print ('EMAIL NOT REGISTERED')
            alerts.append('The email address "{}" is either incorrect or has not been registered'.format(email))
            return (False, alerts)
        else:
            if email == user.email:
                if bcrypt.hashpw(password.encode(), user.pw_hashed.encode()) == user.pw_hashed:
                    print ('PW Match')
                    return (True, user.id, user.username)
                    # return (True, user.id)
                else:
                    print ('NO MATCH')
                    alerts.append('Incorrect password')

            if alerts:
                return (False, alerts)


    def register(self, postData):
        # collect form data to create new user
        username = str(postData['username'])
        email = postData['email']
        password = postData['password']
        pw_verify = postData['pw_verify']

        alerts = []

        try:
            user = User.objects.get(email=email)
        except:
            if len(username) < 2:
                alerts.append('Username must contain at least 2 characters')
            elif not str.isalnum(username):
                alerts.append('Username may only contain letters and numbers')

            if len(email) < 1:
                alerts.append('Email required')
            elif not EMAIL_REGEX.match(email):
                alerts.append('Invalid email address')

            if len(password) < 8:
                alerts.append('Password must be at least 8 characters in length')
            elif password != pw_verify:
                alerts.append('Passwords do not match')

            if alerts:
                return (False, alerts)

            else:
                pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User.objects.create(username=username, email=email, pw_hashed=pw_hashed)
                return (True, user.id, user.username)

        else:
            print ('USER ALREADY EXISTS')
            alerts.append('The email address "{}" has already been registered.'.format(email))
            return (False, alerts)




class User(models.Model):
    username = models.CharField(max_length=75)
    email = models.EmailField(max_length=255, unique=True)
    pw_hashed = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()
    objects = models.Manager()
