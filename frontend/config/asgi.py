import os

# Define o modulo de configuracao usado pelo servidor ASGI.
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Ponto de entrada ASGI do frontend.
application = get_asgi_application()
