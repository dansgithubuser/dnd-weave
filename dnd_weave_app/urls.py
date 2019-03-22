from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

import inspect

def isview(member):
    if not inspect.isfunction(member): return False
    if member.__module__ != 'dnd_weave_app.views': return False
    return True

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='login.html')),
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
    print('{}: /{}'.format(i.lookup_str, i.pattern))
