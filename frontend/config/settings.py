import os
from pathlib import Path

from dotenv import load_dotenv

# Base do projeto usada para localizar o arquivo .env do frontend.
BASE_DIR = Path(__file__).resolve().parent.parent
# Carrega as configuracoes locais do frontend.
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: str = "false") -> bool:
    # Converte texto de ambiente em valor booleano.
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    # Transforma uma string separada por virgulas em lista Python.
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


# Chave secreta do Django usada pelo frontend.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-frontend-dev-key")
# Liga ou desliga o modo de depuracao.
DEBUG = env_bool("DJANGO_DEBUG", "true")
# Lista de hosts autorizados.
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS",
                         "127.0.0.1,localhost") or ["*"]

# Aplicacoes carregadas pelo frontend.
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chat",
]

# Middlewares executados em cada requisicao.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Raiz das rotas do projeto frontend.
ROOT_URLCONF = "config.urls"

# Configuracao padrao de templates.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# Ponto de entrada WSGI do frontend.
WSGI_APPLICATION = "config.wsgi.application"

# Banco local padrao do Django. O frontend nao acessa o MySQL diretamente.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Validadores de senha nao sao usados neste exemplo.
AUTH_PASSWORD_VALIDATORS = []

# Parametros regionais da aplicacao.
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Pasta publica para arquivos estaticos.
STATIC_URL = "static/"
# Tipo padrao de chave primaria.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL do backend que o chat utiliza para enviar mensagens.
BACKEND_CHAT_URL = os.getenv(
    "BACKEND_CHAT_URL", "http://127.0.0.1:8000/api/chat/")
