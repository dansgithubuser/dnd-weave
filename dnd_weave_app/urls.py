from . import views

from rest_framework import routers, viewsets

from django.urls import path, include, resolvers, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

import inspect
import os

def pattern(name, template_name=None, param=None, param_re=r'\d'):
    if not template_name: template_name = '{}.html'.format(name)
    route = '^'
    if name: route += '{}/'.format(name)
    if param: route += '(?:(?P<{}>{}+)/)?'.format(param, param_re)
    route += '$'
    view = TemplateView.as_view(template_name=template_name)
    return re_path(route, view)

urlpatterns = [
    pattern('plaintext_explorer'),
    pattern('login'),
    pattern('secretmaker', param='secret_id'),
    pattern('spellgranter', param='character_id'),
    pattern('character_delver', param='character_id'),
    path('resource/', include('rest_framework.urls', namespace='rest_framework')),
]

router = routers.DefaultRouter()

for name, value in inspect.getmembers(views):
    if getattr(value, '__module__', None) != 'dnd_weave_app.views': continue
    if inspect.isfunction(value):
        route = name
        doc = inspect.getdoc(value)
        if doc:
            doc = eval(doc)
            route = doc.get('route', route)
        urlpatterns.append(path(route, value))
    elif issubclass(value, viewsets.GenericViewSet):
        router.register(name[:-7], value)

urlpatterns.append(path('resource/', include(router.urls)))
