# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.sites.models import Site

def greenhouseview(request, site_name=None):
    args = {}
    if site_name:
        args['site_name'] = site_name

    return render(request, '../gbb/templates/sites/nextgen/greenhouses.html', args)

