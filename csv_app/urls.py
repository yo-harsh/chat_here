from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for rendering the HTML page
    path('csv/', views.render_index, name='render_index'),

    # URL patterns for your views
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('chat_with_bot/', views.chat_with_bot, name='chat_with_bot'),
    # Add other URL patterns as needed
]
