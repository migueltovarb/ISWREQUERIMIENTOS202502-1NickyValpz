"""
Django settings for nikys_coffee_hub project.
"""

from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t95510y76sit-qa-s^kcloy2=tsunwor2ng5a*+b#2h@u+1d8@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: list[str] = []


# -------------------------------------------------------
#   APPS DEL PROYECTO
# -------------------------------------------------------

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps propias
    'dashboard',
    'menu',
    'orders',
]

# Indicar que usaremos nuestro CustomUser
AUTH_USER_MODEL = "dashboard.User"


# -------------------------------------------------------
#   MIDDLEWARE
# -------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -------------------------------------------------------
#   URLS PRINCIPALES
# -------------------------------------------------------

ROOT_URLCONF = 'nikys_coffee_hub.urls'


# -------------------------------------------------------
#   TEMPLATES
# -------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Carpeta global de templates
        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'nikys_coffee_hub.wsgi.application'


# -------------------------------------------------------
#   BASE DE DATOS
# -------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -------------------------------------------------------
#   VALIDACIÓN DE PASSWORDS
# -------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -------------------------------------------------------
#   CONFIGURACIÓN DE IDIOMA Y ZONA HORARIA
# -------------------------------------------------------

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# -------------------------------------------------------
#   ARCHIVOS ESTÁTICOS Y MEDIA
# -------------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# (para collecstatic en producción)
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


# -------------------------------------------------------
#   AUTENTICACIÓN / REDIRECCIONES
# -------------------------------------------------------

# Cuando un @login_required necesite login:
LOGIN_URL = '/dashboard/login/'

# Opcional: adónde enviar después de login/logout
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


# -------------------------------------------------------
#   CONFIGURACIÓN FINAL
# -------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
