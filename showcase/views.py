# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect #, HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from models import Team, Item
from forms import TeamForm, ItemForm


def team(request): #create/update team object
    if Team.objects.filter(user=request.user).exists():
        team = Team.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, instance = team or None)
        if form.is_valid():
            team = form.save(commit=False)
            team.user = request.user
            team.save()
            return HttpResponseRedirect('/dashboard')

    if team:
    	form = TeamForm(instance = team)
    else:
    	form = TeamForm()

    args = {'form' : form}
    #args.update(csrf(request))
    return render(request, 'templates/showcase/team.html', args)

def dashboard(request): #view/delete item objects
    if Team.objects.filter(user=request.user).exists():
        team = Team.objects.get(user=request.user)
    else:
        HttpResponseRedirect('/team')

    items = Item.objects.filter(team=team)
    args = {'team' : team, 'items' : items}
    return render(request, 'templates/showcase/dashboard.html', args)

def item(request, item_id=None): #add/edit item object
    if Team.objects.filter(user=request.user).exists():
        team = Team.objects.get(user=request.user)
    else:
        HttpResponseRedirect('/team')

    args = {}
    if item_id:
        item = Item.objects.get(id=item_id)
        args.update({'item' : item})

    else:
        item = None

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.team = team
            item.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = ItemForm(instance=item)

    args.update({'team' : team})
    args.update({'form' : form})
    #args.update(csrf(request))
    return render(request, 'templates/showcase/item.html', args)

def delete(request, item_id=None): #delete item object
    if item_id:
        item = Item.objects.get(id=item_id)
        item.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')