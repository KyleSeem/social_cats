# -*- coding: utf-8 -*-
# apps/login_reg/views.py

from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

####### NAVIGATION #######

# route to login form - default landing page
def user_login(request):
    # User.objects.all().delete()
    request.session.clear()
    context = {
        'users':User.objects.all()
    }
    return render(request, 'login_reg/login.html', context)

# route to registration form
def reg_form(request):
    request.session.clear()
    context = {
        'users':User.objects.all()
    }
    return render(request, 'login_reg/register.html', context)


# login as guest - read-only access
def guest(request):
    request.session.clear()
    request.session['sessionUserName'] = 'Guest'
    request.session['sessionUserID'] = 0
    return redirect(reverse('social_media:index'))



####### CRUD #######

# login - validate form data
def login(request):
    request.session['log_email'] = request.POST['log_email']

    if request.method == "POST":
        verify = User.userManager.login(request.POST)

        if verify[0] == False:
            for alert in verify[1]:
                messages.add_message(request, messages.INFO, alert)
            return redirect(reverse('login_reg:user_login'))

        elif verify[0] == True:
            request.session.clear()
            request.session['sessionUserID'] = verify[1]
            request.session['sessionUserName'] = verify[2]
            return redirect(reverse('social_media:index'))

    elif request.method == "GET":
        # request.session.clear()
        return redirect(reverse('login_reg:user_login'))


# register - validate form data
def register(request):
    # keep user input in form if user data returns with errors
    request.session['username'] = request.POST['username']
    request.session['email'] = request.POST['email']
    request.session['password'] = request.POST['password']

    if request.method == "POST":
        verify = User.userManager.register(request.POST)

        if verify[0] == False:
            for alert in verify[1]:
                messages.add_message(request, messages.INFO, alert)
            return redirect(reverse('login_reg:reg_form'))

        elif verify[0] == True:
            request.session.clear()
            request.session['sessionUserID'] = verify[1]
            request.session['sessionUserName'] = verify[2]
            return redirect(reverse('social_media:index'))

        else:
            request.session.clear()
            return redirect(reverse('login_reg:reg_form'))


# logout - clear session and return to landing page
def logout(request):
    request.session.flush()
    return redirect(reverse('login_reg:user_login'))


# delete user - called from setting page in user account
def delete(request, id):
    alerts = []
    print id

    if request.method == "POST":
        user = User.objects.get(id=id)
        alerts.append('The account registered under email address "{}" has been deleted'.format(user.email))
        user.delete()
        request.session.clear()
        return redirect(reverse('login_reg:user_login'))
