# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from models import Team, Item
from forms import TeamForm, ItemForm
from hashlib import sha1 #for s3_sign_put
import time, os, urllib, hmac, json, binascii, base64 #for s3_sign_put



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

    args = {}
    args['form'] = form
    args['team'] = team
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
    file_structure = str(os.environ.get('DJANGO_ENV')) + '/teams/'
    if Team.objects.filter(user=request.user).exists():
        team = Team.objects.get(user=request.user)
        file_structure += str(team.template_dir) + '/items/'

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
    args.update({'file_structure' : file_structure})
    #args.update(csrf(request))
    return render(request, 'templates/showcase/item.html', args)

def delete(request, item_id=None): #delete item object
    if item_id:
        item = Item.objects.get(id=item_id)
        item.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')

#response to client side request with signed signature for amazon s3 using environment variable credentials
def sign_s3_put(request):
    #logger = logging.getLogger(__name__)

    s3_bucket_name = os.environ.get('S3_BUCKET')
    s3_access_key = os.environ.get('S3_KEY')
    s3_secret_key = os.environ.get('S3_SECRET')

    object_name = request.GET.get('s3_object_name')
   
    mime_type = request.GET.get('s3_object_type')

    expires = int(time.time()+300)
    amz_headers = "x-amz-acl:public-read"

    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, s3_bucket_name, object_name)

    hashed = hmac.new(s3_secret_key, put_request, sha1)
    signature = binascii.b2a_base64(hashed.digest())[:-1]
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (s3_bucket_name, object_name)

    signed_request = '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, s3_access_key, expires, signature)

    #logger.info('Signature: ' + signature)
    
    return HttpResponse(json.dumps({
    'signed_request': signed_request,
    'url': url
    }), content_type='application/json')