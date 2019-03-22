from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

import math
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'deps', 'dnd', 'dnd'))

import weave

def plaintext_explorer(request):
    return render(request, 'plaintext_explorer.html')

def plaintext_to_dict(request):
    plaintext = [int(i) for i in request.GET['plaintext'].split()]
    d = weave.plaintext_to_dict(plaintext)
    for k in d.keys():
        if d[k] == math.inf:
            d[k] = 'infinity'
    return JsonResponse(d)

def plaintext_extras(request):
    element = request.GET.get('element')
    return JsonResponse(weave.extras[element] if element else weave.misc, safe=False)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    '''{'route': ''}'''
    if request.user.is_authenticated:
        template = 'home.html'
    else:
        template = 'home-guest.html'
    return render(request, template)
