from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from django.contrib import messages
class UserManager(models.Manager):
    def register(self,postData):
        result = {'status':True, 'error':[]}
        if not postData['name'] or postData['name'] < 3:
            result['status'] = False
            result['error'].append('Name must be at least 3 characters')
        if not postData['username'] or postData['username'] < 3:
            result['status'] = False
            result['error'].append('Username must be at least 3 characters')
        if not postData['password'] or postData['password'] < 8:
            result['status'] = False
            result['error'].append('Password must be at least 8 characters')
        if not postData['cpassword'] or postData['cpassword'] != postData['password']:
            result['status'] = False
            result['error'].append('Passwords must match')
        if result['status'] == True:
            if User.objects.filter(username = postData['username']):
                result['status'] = False
                result['error'].append('User already exist')
            else:
                password = postData['password'].encode('utf-8')
                hashedpw = bcrypt.hashpw(password,bcrypt.gensalt(12))
                User.objects.create(
                    name = postData['name'],
                    username = postData['username'],
                    password = hashedpw,
                )
        return result
    def login(self,postData, sessionData):
        user = User.objects.filter(username = postData['username'])
        if len(user) > 0:
            hashed = User.objects.get(username = postData['username']).password.encode('utf-8')
            password = postData['password'].encode('utf-8')
            if bcrypt.hashpw(password,hashed) == hashed:
                sessionData['id'] = User.objects.get(username = postData['username']).id
                return True
            else:
                return False

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()