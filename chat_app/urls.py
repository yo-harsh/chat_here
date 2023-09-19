from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main'),
    path('bot/', views.bot, name='bot'),
    path('message/', views.api_message, name='chat_api'),
    path('key/', views.key, name='api_key')
    
]
