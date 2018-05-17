from django.shortcuts import render
from django.http import HttpResponseRedirect #, HttpResponse, JsonResponse
from django.contrib.auth.models import User #, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from showcase.models import Team, Item
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

#for live sites, checks domain to know which site we are on
def home(request):
    args = {}

    if 'sunstonefarmsoregon' in request.get_host():
        site_name='sunstonefarms'
    elif 'nextgenerationnurseries.com' in request.get_host():
        site_name='nextgennurseries'
    elif 'heartofthevalleyclones.com' in request.get_host():
        site_name='heartoftv'
    else:
        return render(request, 'templates/index.html')

    try:
        current_site = Site.objects.get(name=site_name)
    except Site.DoesNotExist:
        return render(request, 'templates/index.html')

    
    try:
        team = Team.objects.get(site=current_site)
        template = 'templates/sites/' + team.template_dir + '/'
        
        items = Item.objects.filter(team=team)[0:4]
        items = items[::-1] #reverse order

        args['team'] = team
        args['highlights'] = items
        return render(request, template+'index.html', args)
    
    except Team.DoesNotExist:
        return render(request, 'templates/index.html')

#for development purposes only
def sites(request, site_name=None):
    args = {}
    if site_name:
        args['site_name'] = site_name
    else:
        return HttpResponseRedirect('/')

    try:
        current_site = Site.objects.get(name=site_name)
    except Site.DoesNotExist:
        return HttpResponseRedirect('/')

    
    try:
        team = Team.objects.get(site=current_site)
        template = 'templates/sites/' + team.template_dir + '/'
        
        items = Item.objects.filter(team=team)[0:4]
        items = items[::-1]

        args['team'] = team
        args['highlights'] = items
        return render(request, template+'index.html', args)
    
    except Team.DoesNotExist:
        return HttpResponseRedirect('/')


def showcase(request, site_name=None):    
    args = {}
    if site_name:
        args['site_name'] = site_name
    else:
        site_name = ''
        if 'sunstonefarmsoregon' in request.get_host():
            site_name='sunstonefarms'

    try:
        current_site = Site.objects.get(name=site_name)
    except Site.DoesNotExist:
        return HttpResponseRedirect('/')

    
    team = Team.objects.get(site=current_site)
    template = 'templates/sites/' + team.template_dir + '/'
    items = Item.objects.filter(team=team)
    items = items[::-1]
    
    args['team'] = team
    args['items'] = items
    return render(request, template+'showcase.html', args)

def about(request, site_name=None):    
    args = {}
    if site_name:
        args['site_name'] = site_name
    else:
        site_name = ''
        if 'sunstonefarmsoregon' in request.get_host():
            site_name='sunstonefarms'

    try:
        current_site = Site.objects.get(name=site_name)
    except Site.DoesNotExist:
        return HttpResponseRedirect('/')
    
    team = Team.objects.get(site=current_site)
    template = 'templates/sites/' + team.template_dir + '/'
    items = Item.objects.filter(team=team)

    args['team'] = team
    return render(request, template+'about.html', args)

def contact(request, site_name=None):    
    args = {}
    if site_name:
        args['site_name'] = site_name
    else:
        site_name = ''
        if 'sunstonefarmsoregon' in request.get_host():
            site_name='sunstonefarms'

    try:
        current_site = Site.objects.get(name=site_name)
    except Site.DoesNotExist:
        return HttpResponseRedirect('/')

    team = Team.objects.get(site=current_site)
    template = 'templates/sites/' + team.template_dir + '/'    

    args['team'] = team
    return render(request, template+'contact.html', args)

def contact_us(request):
    return render(request, 'templates/contact_us.html')

# def services(request):
#     return render(request, 'templates/services.html')

def auth_view(request):
    username = request.POST.get('username', '').lower()
    password = request.POST.get('password', '')

    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.info(request, 'bad username')
        return HttpResponseRedirect('/login')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        if Team.objects.filter(user=user).exists():
            team = Team.objects.get(user=request.user)
            if team.address1:
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponseRedirect('/team')
        else:
            return HttpResponseRedirect('/team')
    else:
        messages.info(request, 'bad password')
        return HttpResponseRedirect('/login')

def login_view(request):
    if request.user.is_authenticated():
        if Team.objects.filter(user=request.user).exists():
            team = Team.objects.get(user=request.user)
            if team.address1:
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponseRedirect('/team')
        else:
            return HttpResponseRedirect('/team')

    storage = messages.get_messages(request)
    for m in storage:
        if 'bad password' in m.message:
            args = {'code': 'bad_pass',}
            return render(request, 'templates/login.html', args)
        elif 'bad username' in m.message:
            args = {'code': 'bad_user',}
            return render(request, 'templates/login.html', args)

    return render(request, 'templates/login.html')

def logout_view(request):
    logout(request)
    # messages.info(request, 'from logout') #message to tell user they just logged out on home page redirect
    return HttpResponseRedirect('/')
