# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Trip
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id = request.session['id'])
    context = {
        "user": user,
        "trips": Trip.objects.filter(Q(created = user) | Q(user = user)),
        "other": Trip.objects.exclude(Q(created = user) | Q(user = user)),
    }
    return render(request, "tripapp/index.html", context)
def add(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    return render(request, 'tripapp/add.html')
def addTrip(request):
    user = User.objects.get(id = request.session['id'])
    result = Trip.objects.createTrip(request.POST, user)
    if result['status'] == False:
        for error in result['error']:
            messages.error(request, error)
        return redirect(reverse("tripapp:add"))
    return redirect(reverse("tripapp:index"))
def view(request, trip_id):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id = request.session['id'])
    trip = Trip.objects.get(id = trip_id)
    context = { 
        "trip" : trip,
        "goers" : trip.user.all()
    }
    return render(request, 'tripapp/view.html', context)
def join(request, trip_id):
    trip = Trip.objects.get(id = trip_id)
    trip.user.add(User.objects.get(id = request.session['id']))
    return redirect(reverse('tripapp:index'))
def logout(request):
    request.session.pop('id')
    return redirect(reverse("loginapp:index"))
