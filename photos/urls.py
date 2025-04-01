from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'photos'
urlpatterns = [
    path('photos/', views.gallery_view, name='gallery_photos'), 
    path('photos/<int:gallery_id>/', views.une_gallery_view, name='gallery_view'),
    
]