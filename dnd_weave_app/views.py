from . import models
from . import serializers
from . import helpers

import weave

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import json

def plaintext_to_dict(request):
    plaintext = [int(i) for i in request.GET['plaintext'].split(',')]
    d = helpers.plaintext_to_jsonable(plaintext)
    return JsonResponse(d)

def plaintext_extras(request):
    element = request.GET.get('element')
    return JsonResponse(weave.extras[element] if element else weave.misc, safe=False)

def home(request):
    '''{'route': ''}'''
    context = {'secrets': [], 'spellgrantees': [], 'characters': []}
    if request.user.is_authenticated:
        context['secrets'] = SecretViewSet.list_internal(request)
        context['spellgrantees'] = CharacterViewSet.spellgrantees_internal(request)
        context['characters'] = CharacterViewSet.list_internal(request)
        for k, v in context.items():
            for i in v:
                if not i['name']: i['name'] = i['id']
    return render(request, 'home.html', context)

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

def ciphertext_to_runes(request):
    ciphertext = [int(i) for i in request.GET['ciphertext'].split(',')]
    serialized = models.Secret.objects.get(
        id=request.GET['secret_id'],
        keeper=request.user,
    ).serialized
    secret = weave.Secret().deserialize(serialized)
    runes = weave.ciphertext_to_runes(ciphertext, secret)
    return JsonResponse(runes, safe=False)

def ciphertext_to_plaintext(request):
    ciphertext = [int(i) for i in request.GET['ciphertext'].split(',')]
    serialized = models.Secret.objects.get(
        id=request.GET['secret_id'],
        keeper=request.user,
    ).serialized
    secret = weave.Secret().deserialize(serialized)
    plaintext = weave.ciphertext_to_plaintext(ciphertext, secret)
    return JsonResponse(plaintext, safe=False)

class SecretPermission(permissions.BasePermission):
    def has_permission(self, request, view, secret):
        return secret.keeper == request.user

class SecretViewSet(viewsets.ModelViewSet):
    queryset = models.Secret.objects.all()
    serializer_class = serializers.SecretSerializer

    def perform_create(self, serializer):
        serializer.save(
            keeper=self.request.user,
            serialized=weave.Secret().serialize(),
        )

    def perform_update(self, serializer):
        if len(models.Character.objects.filter(secret_id=self.get_object().id)):
            raise Exception('secret has already been accepted by a character, cannot change it')
        secret = weave.Secret().deserialize(self.request.data['serialized'])
        serializer.save(serialized=secret.serialize())

    @classmethod
    def list_internal(cls, request):
        secrets = models.Secret.objects.filter(keeper_id=request.user.id).order_by('id')
        serializer = cls.serializer_class(secrets, many=True)
        return serializer.data

    def list(self, request):
        return Response(self.list_internal(request))

def offer(request):
    post = json.loads(request.body)
    player = User.objects.get(username=post['player'])
    name_or_id = post['character_name']
    q = Q(name=name_or_id)
    if name_or_id.isdigit(): q |= Q(id=post['character_name'])
    character = models.Character.objects.get(Q(player=player), q)
    models.Offer.objects.create(
        secret_id=post['secret_id'],
        character=character,
    )
    return HttpResponse(status=201)

def accept(request):
    post = json.loads(request.body)
    offer = models.Offer.objects.get(id=post['offer_id'])
    models.Character.objects.filter(
        id=post['character_id'],
        player=request.user,
    ).update(secret_id=offer.secret_id)
    return HttpResponse(status=204)

class CharacterPermission(permissions.BasePermission):
    def has_permission(self, request, view, character):
        return character.player == request.user

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    @classmethod
    def list_internal(cls, request):
        characters = models.Character.objects.filter(player_id=request.user.id).order_by('id')
        serializer = cls.serializer_class(characters, many=True)
        return serializer.data

    def list(self, request):
        return Response(self.list_internal(request))

    def retrieve(self, request, pk):
        character = models.Character.objects.get(id=pk)
        data = self.get_serializer(character).data
        offers = models.Offer.objects.filter(character=character).values('id', 'secret__id', 'secret__name')
        data['offers'] = [{
            'id': i['id'],
            'secret': {
                'id': i['secret__id'],
                'name': i['secret__name'],
            },
        } for i in offers]
        return Response(data)

    @classmethod
    def spellgrantees_internal(cls, request):
        characters = models.Character.objects.filter(secret__keeper=request.user)
        serializer = cls.serializer_class(characters, many=True)
        return serializer.data

    @action(detail=False)
    def spellgrantees(self, request):
        return Response(self.spellgrantees_internal(request))

def research(request):
    post = json.loads(request.body)
    character = models.Character.objects.get(id=post['character_id'])
    if character.player_id != request.user.id:
        raise Exception("character doesn't belong to user")
    models.Spell.objects.create(
        character_id=character.id,
        runes=post['runes'],
    )
    return HttpResponse(status=201)

def spells(request):
    character = models.Character.objects.get(id=request.GET['character_id'])
    if character.player != request.user:
        secret = models.Secret.get(id=character.secret_id)
        if secret.keeper != request.user:
            raise Exception("character doesn't belong to and isn't secret-kept by user")
    spells = models.Spell.objects.filter(character_id=request.GET['character_id']).values('id', 'runes', 'dict').order_by('id')
    return JsonResponse([
        {'id': i['id'], 'runes': i['runes'], 'dict': json.loads(i['dict']) if i['dict'] else ''}
        for i in spells
    ], safe=False)

def grant(request):
    #homogenize data
    if request.method == 'POST':
        data = json.loads(request.body)
    else:
        data = request.GET
    #get or create spell
    spell_id = data.get('spell_id')
    if spell_id:
        spell = models.Spell.objects.get(id=spell_id)
    else:
        spell = models.Spell(
            character_id=data['character_id'],
            runes=data['runes'],
        )
    #check permission
    character = models.Character.objects.filter(id=spell.character_id).values('secret__serialized', 'secret__keeper_id')[0]
    if request.user.id != character['secret__keeper_id']:
        raise Exception("user isn't secret keeper for this spell")
    #decrypt
    secret = weave.Secret().deserialize(character['secret__serialized'])
    try:
        ciphertext = weave.runes_to_ciphertext(spell.runes.split(), secret)
    except:
        return JsonResponse({'not a spell': 'invalid runes'})
    plaintext = weave.ciphertext_to_plaintext(ciphertext, secret)
    d = helpers.plaintext_to_jsonable(plaintext)
    #custom level
    level = data.get('level')
    if level is not None: d['level'] = int(level)
    #results
    spell.dict = json.dumps(d)
    if request.method == 'POST': spell.save()
    return JsonResponse(d)

def runes_to_dict(request):
    secret = models.Secret.objects.get(id=request.GET['secret_id'])
    if request.user.id != secret.keeper_id:
        raise Exception("user isn't keeper of this secret")
    secret = weave.Secret().deserialize(secret.serialized)
    ciphertext = weave.runes_to_ciphertext(request.GET['runes'].split(), secret)
    plaintext = weave.ciphertext_to_plaintext(ciphertext, secret)
    d = helpers.plaintext_to_jsonable(plaintext)
    return JsonResponse(d)
