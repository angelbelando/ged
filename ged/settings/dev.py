from .base import *

SECRET_KEY = '2oct_bcq26rqqawm%7t9p+tbxnr674@c6#v1$)dr7tzf312c0c'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','serveur','192.168.1.24' ]

# INSTALLED_APPS += ['debug_toolbar', 'django_extensions',]

# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]

# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

# INTERNAL_IPS = '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'bd_ged', # le nom de notre base de donnees creee precedemment
        'USER': 'angel', # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': 'angel',
        'HOST': '',
        'PORT': '5432',
    }
}