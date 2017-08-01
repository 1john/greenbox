from django.shortcuts import render
from django.http import HttpResponseRedirect #, HttpResponse, JsonResponse
from django.contrib.auth.models import User #, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, 'templates/index.html')

def contact(request):
    return render(request, 'templates/contact.html')

# def login(request):
#     return render(request, 'templates/login.html')

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
        #return HttpResponseRedirect('/dashboard/' + User.team.name)
        return HttpResponseRedirect('/dashboard/')
    else:
        messages.info(request, 'bad password')
        return HttpResponseRedirect('/login')

def login_view(request):
    if request.user.is_authenticated():
        #return HttpResponseRedirect('/dashboard/' + User.team.name)
        return HttpResponseRedirect('/dashboard/')

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

def dashboard(request):
    #add/edit/delete "items"

    #team = request.user.team.name
    team = "team name here"

    args = {'team' : team}
    return render(request, 'templates/dashboard.html', args)

def services(request):
    return render(request, 'templates/services.html')