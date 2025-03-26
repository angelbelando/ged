from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'papiers'
urlpatterns = [
    path('documents/', views.DocumentListView.as_view(), name='liste_documents'), 
    path('documents/<int:pk>/', views.DocumenttDetailView.as_view(), name='detail_document'),
    path('thumbnail/<int:document_id>/', views.generate_thumbnail, name='generate_thumbnail'),
]