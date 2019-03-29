from . import views

from rest_framework import routers, viewsets

from django.urls import path, include, resolvers
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

import inspect
import os

urlpatterns = [
    path('plaintext_explorer', TemplateView.as_view(template_name='plaintext_explorer.html')),
    path('login', auth_views.LoginView.as_view(template_name='login.html')),
    path('', TemplateView.as_view(template_name='home.html')),
    path('secretmaker', TemplateView.as_view(template_name='secretmaker.html')),
    path('character_delver', TemplateView.as_view(template_name='character_delver.html')),
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
