from django.urls import path
from . import views

urlpatterns = [
    # # URL pattern for rendering the HTML page
    path('csv/', views.render_index, name='render_index'),

    # URL patterns for your views
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('csv_agent/', views.csv_agent, name='csv_agent'),
    # Add other URL patterns as needed
]