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
from django.contrib.auth import views as auth_views
from recettes.views import signup_view, logout_view

app_name = 'recettes'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('manage/', views.manage, name='manage'),
    path('add_category/', views.add_category, name='add_category'),
    path('recette/<int:pk>', views.details, name='details'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('toggle_favoris/<int:pk>', views.toggle_favoris, name='toggle_favoris'),
    path('favoris/', views.fav_view, name='favoris'),
    path('recette/<int:pk>/modifier/', views.modifier_recette, name='modifier_recette'),
    path('recette/<int:recette_id>/note/', views.ajouter_note, name='ajouter_note'),
    path('tendances/', views.recettes_tendances, name='recettes_tendances'),
]
