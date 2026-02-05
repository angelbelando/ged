"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recettes import views

app_name = 'recettes'
urlpatterns = [
    path('', views.RecetteListView.as_view(), name='recettes'),
    path('<int:pk>/', views.RecetteDetailView.as_view(), name='detail'),
    path('<int:pk>/export-docx/', views.ExportRecetteDocxView.as_view(), name='export_docx'),
    path("<int:pk>/pdf/", views.ExportRecettePDFView.as_view(), name="recette_pdf"),
    path('new/', views.RecetteCreateView.as_view(), name='recette_create'),
    path('<int:pk>/edit/', views.RecetteUpdateView.as_view(), name='recette_update'),

]
