from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6p@g8t8jtk_f)dox#=b(@*b)omwgsl1uvr$ad0_y6#x2hh+c46'


#lenguajes del humanize
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

#idioma por defecto en espa;ol
LANGUAGE_CODE = 'es'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #bibliotecas instaladas
    'tailwind', #python manage.py tailwind init
    'theme',#python manage.py tailwind install *(recordar lo del modo oscuro en theme)
    'crispy_forms',
    "crispy_tailwind",
    #usuarios
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.humanize',
    #apps instaladas
    'users',
    'admins',
    'managers',
    'information',
    'teachers',
    'guardians',
    'students',
]
#python manage.py runserver_plus --cert-file cert.crt --key-file key.key
SECURE_CROSS_ORIGIN_OPENER_POLICY = None


#AGREGAR NODE JS A NUESTRO ENTORNO DE TRABAJO (recuerda agregarlo al path)
#############################################################################
#Windows
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
#Ubuntu


NPM_BIN_PATH ="/home/miguel/.nvm/versions/node/v22.15.0/bin/npm" # whereis npm
#############################################################################

#autenticacion de usuario...
SITE_ID = 1

#esto es para los usuarios abstractos 
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = "/redirect/"


#externo de tailwind
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
    '0.0.0.0',
]#despues de ahcer esto colocar #python manage.py tailwind install


CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'PanelParaColegiosMKDJF.sqlite3',
    }
}



#usuarios
AUTHENTICATION_BACKENDS = (
    #'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'

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

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



"""
es - AJUSTES DE SEGURIDAD
en - SECURITY SETTINGS
"""

# Redirigir a HTTPS desactivado
SECURE_SSL_REDIRECT = False

# Cookies no seguras (para desarrollo local)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# HSTS desactivado (para desarrollo local)
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Proxy SSL desactivado (si no usas un proxy en local)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Protección adicional contra XSS y MIME desactivado (opcional para desarrollo)
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

# Configuración adicional de cookies (solo en desarrollo)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True


# Permitir que se puedan incrustar los archivos en un iframe
X_FRAME_OPTIONS = "SAMEORIGIN"

