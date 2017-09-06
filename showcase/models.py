# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Team(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=128)
	address1 = models.CharField(blank=True, max_length=64)
    address2 = models.CharField(blank=True, max_length=64)
    city = models.CharField(blank=True, max_length=64)
    state = models.CharField(blank=True, max_length=2)
    zip_code = models.CharField(max_length=5, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
