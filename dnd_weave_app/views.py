from django.http import JsonResponse
from django.shortcuts import render

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

def extras(request):
    element = request.GET.get('element')
    return JsonResponse(weave.extras[element] if element else weave.misc, safe=False)
