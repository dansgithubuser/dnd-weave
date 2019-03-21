from django.urls import path
from . import views

import inspect

def isview(member):
    if not inspect.isfunction(member): return False
    if member.__module__ != 'dnd_weave_app.views': return False
    args = inspect.getargspec(member).args
    if len(args) == 0: return False
    if args[0] != 'request': return False
    return True

urlpatterns = [path(name, value) for name, value in inspect.getmembers(views, isview)]
