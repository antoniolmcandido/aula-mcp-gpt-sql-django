import os

from django.core.wsgi import get_wsgi_application

# Define o modulo de configuracao usado pelo servidor WSGI.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Ponto de entrada WSGI do backend.
application = get_wsgi_application()
