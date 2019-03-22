from . import models

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Model
from django.db.models.query import QuerySet

import datetime
import json

def jsonify(value):
    if isinstance(value, datetime.datetime):
        value = value.isoformat()
    elif isinstance(value, Model):
        value = {k: jsonify(v) for k, v in value.__dict__.items() if k != '_state'}
    elif isinstance(value, QuerySet):
        value = [jsonify(i) for i in value]
    #else: print('{} jsonify: missing clause for {}'.format(__file__, type(value))
    return value

def json_responsify(value):
    return JsonResponse(jsonify(value), safe=False)

def upper_camel_case(name):
    return ''.join([i.capitalize() for i in name.replace('_', '-').split('-')])

def add(urlpatterns, name, user_id_field='user_id'):
    model = getattr(models, upper_camel_case(name))

    def user_objects(request):
        return model.objects.filter(**{ user_id_field: request.user.id })

    def clean(params, model): return {
        k: v
        for k, v in params.items()
        if k in [i.name for i in model._meta.get_fields()]
            and k != user_id_field
    }

    @login_required
    def cr(request):
        if request.method == 'POST':
            params = clean(request.POST, model)
            params[user_id_field] = request.user.id
            instance = model.objects.create(**params)
            return json_responsify(instance)
        else:
            return json_responsify(user_objects(request))

    @login_required
    def rud(request, id):
        filter_args = { user_id_field: request.user.id }
        if request.method == 'PATCH':
            params = json.loads(request.body)
            params = clean(params, model)
            return json_responsify(user_objects(request).filter(id=id).update(**params))
        elif request.method == 'DELETE':
            return json_responsify(user_objects(request).get(id=id).delete())
        else:
            return json_responsify(user_objects(request).get(id=id))

    urlpatterns.extend([
        path(name, cr),
        path(name + '/<int:id>', rud),
    ])
