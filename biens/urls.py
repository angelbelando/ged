from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'biens'
urlpatterns = [
    
    path('objets/', views.ObjetListView.as_view(), name='liste_objets'),
    
    path('objets/<int:pk>/', views.ObjetDetailView.as_view(), name='detail_objet'),
    
    # path('<pk>', views.DetailFilm.as_view(), name='detail'),
]