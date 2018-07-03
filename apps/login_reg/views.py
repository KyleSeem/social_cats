# -*- coding: utf-8 -*-
# login_reg
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User


# Create your views here.
def index(request):
    # User.objects.all().delete()

    context = {
        'users':User.objects.all()
    }
    return render(request, 'login_reg/index.html', context)


def login(request):
    request.session['log_email'] = request.POST['log_email']

    if request.method == "POST":
        verify = User.userManager.login(request.POST)

        if verify[0] == False:
            for alert in verify[1]:
                messages.add_message(request, messages.INFO, alert)
            return redirect(reverse('login_reg:index'))

        elif verify[0] == True:
            request.session.clear()
            request.session['sessionUserID'] = verify[1]
            request.session['sessionUserName'] = verify[2]
            # may switch method for this later
            request.session['pID'] = 0
            return redirect(reverse('social_media:index'))

    elif request.method == "GET":
        # request.session.clear()
        return redirect(reverse('login_reg:index'))



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
            return redirect(reverse('login_reg:index'))

        elif verify[0] == True:
            request.session.clear()
            request.session['sessionUserID'] = verify[1]
            request.session['sessionUserName'] = verify[2]
            # may switch method for this later
            request.session['pID'] = 0
            return redirect(reverse('social_media:index'))

        else:
            request.session.clear()
            return redirect(reverse('login_reg:index'))


def show(request, id):
    print



def logout(request):
    request.session.flush()
    return redirect(reverse('login_reg:index'))


def delete(request, id):
    alerts = []
    print id

    if request.method == "POST":
        user = User.objects.get(id=id)
        alerts.append('The account registered under email address "{}" has been deleted'.format(user.email))
        user.delete()
        request.session.clear()
        return redirect(reverse('login_reg:index'))
