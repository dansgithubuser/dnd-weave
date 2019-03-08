from django.urls import path
from . import views

urlpatterns=[
    path('plaintext_explorer', views.plaintext_explorer),
    path('plaintext_to_english', views.plaintext_to_english),
]