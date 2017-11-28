# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Event, Activity, Goal
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id = request.session['id'])
    context = {
        "user": user,
        "events": Event.objects.filter(Q(created = user) | Q(user = user)),
        "other": Event.objects.exclude(Q(created = user) | Q(user = user)),
    }
    return render(request, "eventapp/index.html", context)
def add(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    return render(request, 'eventapp/add.html')
def addevent(request):
    user = User.objects.get(id = request.session['id'])
    result = Event.objects.createEvent(request.POST, user)
    if result['status'] == False:
        for error in result['error']:
            messages.error(request, error)
        return redirect(reverse("eventapp:add"))
    return redirect(reverse("eventapp:index"))
def addactivity(request, event_id):
    user = User.objects.get(id = request.session['id'])
    event = Event.objects.get(id = event_id)
    result = Activity.objects.createActivity(request.POST, user, event)
    if result['status'] == False:
        for error in result['error']:
            messages.error(request, error)
        # return redirect(reverse("eventapp:add"))
    return redirect(reverse("eventapp:index"))
def addgoal(request, event_id):
    user = User.objects.get(id = request.session['id'])
    event = Event.objects.get(id = event_id)
    result = Goal.objects.createGoal(request.POST, user, event)
    if result['status'] == False:
        for error in result['error']:
            messages.error(request, error)
        # return redirect(reverse("eventapp:add"))
    return redirect(reverse("eventapp:index"))
def view(request, event_id):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id = request.session['id'])
    event = Event.objects.get(id = event_id)
    context = { 
        "event" : event,
        "goers" : event.user.all(),
        "activities" : Activity.objects.filter(created = user).filter(event = event),
        "personalgoal" : Goal.objects.filter(created = user).filter(event = event),
    }
    print(Goal.objects.filter(created = user).filter(event = event).count())
    return render(request, 'eventapp/view.html', context)
def join(request, event_id):
    event = Event.objects.get(id = event_id)
    event.user.add(User.objects.get(id = request.session['id']))
    return redirect(reverse('eventapp:index'))
def logout(request):
    request.session.pop('id')
    return redirect(reverse("loginapp:index"))
