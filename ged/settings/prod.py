from .base import *

SECRET_KEY = 'q1eXSi5`IVn\\drJr[\x0c)5{xc!'

DEBUG = False

ALLOWED_HOSTS = ['164.92.250.136']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'bd_ged', # le nom de notre base de donnees creee precedemment
        'USER': 'angel', # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': '***********',
        'HOST': '',
        'PORT': '5432',
    }
}