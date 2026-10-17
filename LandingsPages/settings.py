"""
Django settings for LandingsPages project (Django 6.1).

Desarrollo: no necesitas definir nada, funciona tal cual.
Producción: define estas variables de entorno en el servidor:
    DJANGO_DEBUG=0
    DJANGO_SECRET_KEY=<clave larga y aleatoria>
    DJANGO_ALLOWED_HOSTS=tudominio.com,www.tudominio.com
    EMAIL_HOST_USER=tucorreo@gmail.com
    EMAIL_HOST_PASSWORD=<contraseña de aplicación de Google>
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Modo (desarrollo / producción)
# ---------------------------------------------------------------------------
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

if DEBUG:
    SECRET_KEY = "django-insecure-solo-para-desarrollo"
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
else:
    # En producción NO hay valor por defecto: si falta, el servidor no arranca.
    try:
        SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
        ALLOWED_HOSTS = [h.strip() for h in os.environ["DJANGO_ALLOWED_HOSTS"].split(",") if h.strip()]
    except KeyError as faltante:
        raise ImproperlyConfigured(f"Falta la variable de entorno {faltante} en producción.")

    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS]

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Empieza con 1 hora. Súbelo (p. ej. 31536000) cuando confirmes que todo funciona por HTTPS.
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

    # Descomenta si tu hosting pone un proxy delante (Render, Railway, Nginx...):
    # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ---------------------------------------------------------------------------
# Aplicaciones y middleware
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app.apps.AppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "LandingsPages.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LandingsPages.wsgi.application"


# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ---------------------------------------------------------------------------
# Contraseñas
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# Login del panel
# ---------------------------------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "panel"
LOGOUT_REDIRECT_URL = "login"


# ---------------------------------------------------------------------------
# Idioma y zona horaria (las fechas del panel y del CSV salen en hora de Colombia)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Archivos estáticos
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "app" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # destino de `python manage.py collectstatic`


# ---------------------------------------------------------------------------
# Correo (Django 6.1: MAILERS reemplaza a EMAIL_BACKEND y los EMAIL_* sueltos)
# ---------------------------------------------------------------------------
if DEBUG:
    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.console.EmailBackend",
        },
    }
else:
    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
            "OPTIONS": {
                "host": "smtp.gmail.com",
                "port": 587,
                "use_tls": True,
                "username": os.environ.get("EMAIL_HOST_USER", ""),
                "password": os.environ.get("EMAIL_HOST_PASSWORD", ""),
            },
        },
    }
SILENCED_SYSTEM_CHECKS = ["security.W005", "security.W021"]