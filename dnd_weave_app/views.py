from django.http import JsonResponse
from django.shortcuts import render

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'deps', 'dnd', 'dnd'))

import weave

def plaintext_explorer(request):
    return render(request, 'plaintext_explorer.html')

def plaintext_to_english(request):
    plaintext = [int(i) for i in request.GET['plaintext'].split()]
    english = weave.plaintext_to_english(plaintext)
    return JsonResponse({'english': english})
