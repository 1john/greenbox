from django.shortcuts import render

def home(request):
    return render(request, 'templates/index.html')

def contact(request):
    return render(request, 'templates/contact.html')

def login(request):
    return render(request, 'templates/login.html')
