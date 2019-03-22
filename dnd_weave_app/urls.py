from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

import inspect

def isview(member):
    if not inspect.isfunction(member): return False
    if member.__module__ != 'dnd_weave_app.views': return False
    return True

urlpatterns = [
    path('plaintext_explorer', TemplateView.as_view(template_name='plaintext_explorer.html')),
    path('login', auth_views.LoginView.as_view(template_name='login.html')),
    path('', TemplateView.as_view(template_name='home.html')),
]
for name, value in inspect.getmembers(views, isview):
    route = name
    doc = inspect.getdoc(value)
    if doc:
        doc = eval(doc)
        route = doc.get('route', route)
    urlpatterns.append(path(route, value))

print('serving the following...')
for i in urlpatterns:
    view = i.lookup_str
    if view.endswith('TemplateView'):
        view += '({})'.format(i.callback.view_initkwargs['template_name'])
    print('{}: /{}'.format(view, i.pattern))
