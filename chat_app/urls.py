from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main'),
    path('pdf/', views.pdf, name='pdf'),
    path('message/', views.api_message, name='chat_api')
    
]
