# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..loginapp .models import User
from django.db import models

# Create your models here.
class EventManager(models.Manager):
    def createEvent(self, postData, user):
        result = {'status':True, 'error':[]}
        if not postData['destination']:
            result['status'] = False
            result['error'].append('Destination is empty')
        if not postData['description'] or postData['description'] < 3:
            result['status'] = False
            result['error'].append('Please enter a description')
        if not postData['travel_from']:
            result['status'] = False
            result['error'].append('Enter event start date')
        if not postData['travel_to']:
            result['status'] = False
            result['error'].append('Enter event end date')
        if postData['travel_to'] < postData['travel_from']:
            result['status'] = False
            result['error'].append('End date is before Start date, please try again')
        if result['status'] == True:
            Event.objects.create(
                destination = postData['destination'],
                description = postData['description'],
                travel_from = postData['travel_from'],
                travel_to = postData['travel_to'],
                created = user
            )
        return result

class Event(models.Model):
    destination = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    travel_from = models.DateField()
    travel_to = models.DateField()
    created = models.ForeignKey(User)
    user = models.ManyToManyField(User, related_name='events')
    objects = EventManager()    

class ActivityManager(models.Manager):
    def createActivity(self, postData, user, event):
        result = {'status':True, 'error':[]}
        if not postData['note']:
            result['status'] = False
            result['error'].append('Enter note')
        if not postData['distance']:
            result['status'] = False
            result['error'].append('Enter distance')
        if result['status'] == True:
            Activity.objects.create(
                note = postData['note'],
                distance = postData['distance'],
                created = user,
                event = event
            )
        return result

class Activity(models.Model):
    note = models.CharField(max_length=50)
    distance = models.CharField(max_length=50)
    created = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    objects = ActivityManager()    

class GoalManager(models.Manager):
    def createGoal(self, postData, user, event):
        result = {'status':True, 'error':[]}
        if not postData['goal']:
            result['status'] = False
            result['error'].append('Enter goal')
        if result['status'] == True:
            Goal.objects.create(
                goal = postData['goal'],
                created = user,
                event = event
            )
        return result

class Goal(models.Model):
    goal = models.CharField(max_length=50)
    created = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    objects = GoalManager() 