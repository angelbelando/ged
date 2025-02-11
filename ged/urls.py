"""
URL configuration for ged project.

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
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView
from documents import views as documents_views
from biens import views as biens_views 
from django.conf.urls.static import static
from django.views import generic
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', biens_views.home, name='home'),
    path('objets/', include('biens.urls', namespace='objets')),
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('protected/', biens_views.ProtectedView.as_view(), name='protected'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
