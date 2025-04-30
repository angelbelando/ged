from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'photos'
urlpatterns = [
    path('galleries/', views.GalleryListView.as_view(), name="gallery_list"),
    path('galleries/<slug:slug>/', views.GalleryDetailView.as_view(), name="gallery_detail"),
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(), name="photo_detail"),
]