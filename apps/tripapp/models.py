# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..loginapp .models import User
from django.db import models
import datetime
from dateutil.parser import parse as parse_date

# Create your models here.
class TripManager(models.Manager):
    def createTrip(self, postData, user):
        result = {'status':True, 'error':[]}
        if not postData['destination']:
            result['status'] = False
            result['error'].append('Destination is empty')
        if not postData['description'] or postData['description'] < 3:
            result['status'] = False
            result['error'].append('Please enter a description')
        if not postData['travel_from']:
            result['status'] = False
            result['error'].append('Enter trip start date')
        if not postData['travel_to']:
            result['status'] = False
            result['error'].append('Enter trip end date')
        if postData['travel_to'] < postData['travel_from']:
            result['status'] = False
            result['error'].append('End date is before Start date, please try again')
        if result['status'] == True:
            Trip.objects.create(
                destination = postData['destination'],
                description = postData['description'],
                travel_from = postData['travel_from'],
                travel_to = postData['travel_to'],
                created = user
            )
        return result

class Trip(models.Model):
    destination = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    travel_from = models.DateField()
    travel_to = models.DateField()
    created = models.ForeignKey(User)
    user = models.ManyToManyField(User, related_name='trips')
    objects = TripManager()    
