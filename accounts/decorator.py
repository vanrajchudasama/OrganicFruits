from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponseRedirect

def is_unauthenticated(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
        ...
    else:
       return HttpResponseRedirect('/login')