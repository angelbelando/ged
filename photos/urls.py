from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'photos'
urlpatterns = [
    path('photos/', views.gallery_view, name='gallery_photos'), 
]