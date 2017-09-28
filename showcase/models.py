from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Team(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=128)
    address1 = models.CharField(blank=True, max_length=64)
    address2 = models.CharField(blank=True, max_length=64)
    city = models.CharField(blank=True, max_length=64)
    state = models.CharField(blank=True, max_length=2)
    zip_code = models.CharField(blank=True, max_length=5)
    phone_number = models.CharField(blank=True, max_length=10)
    
    site = models.OneToOneField(Site)
    template_dir = models.CharField(blank=True, max_length=64)

    def __str__(self): #how it shows up in django admin
        return self.name

class Item(models.Model):
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=128)
    img_url = models.CharField(max_length=128)
    thumbnail = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=4096, blank=True)

    def __str__(self): #how it shows up in django admin
        return self.team.name + ' : ' + self.name 