from pathlib import Path
import environ
env = environ.Env()
environ.Env.read_env('.env')
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS = ['https://toledano.org', 'https://www.toledano.org'] 
CORS_ORIGIN_WHITELIST = ['https://toledano.org', 'https://www.toledano.org']


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
]
THIRD_PARTY_APPS = [
    'taggit',
]
LOCAL_APPS = [
    'blog.apps.BlogConfig',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'blogApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogApp.wsgi.application'

DATABASES = {
    'default': env.db(),
}

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

LANGUAGE_CODE = env('DJANGO_LOCALE', default='es-mx')
TIME_ZONE = env('DJANGO_TIME_ZONE', default='America/Mexico_City')
USE_I18N = env('USE_I18N', default=True)
USE_L10N = env('USE_L10N', default=True)
USE_TZ = env('USE_TZ', default=True)
SITE_ID = env('SITE_ID', default=1)

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    'static',     # your static/ files folder
    'blog/static',
]
STATIC_ROOT = 'assets'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Taggit
# django-taggit
# https://django-taggit.readthedocs.io/en/latest/index.html
TAGGIT_CASE_INSENSITIVE = True
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True
