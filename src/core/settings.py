from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-x1u465wiyq6mc&y7h2ds-61gk^pcsy1!3#ht+ic5lihlpcr0bb' # noqa ignore

DEBUG = True

ALLOWED_HOSTS = [
    'transfer.aleksdev.space'
]
CSRF_TRUSTED_ORIGINS = ['https://transfer.aleksdev.space']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'modeltranslation',
    'widget_tweaks',
    'apps.transfer'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa ignore
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa ignore
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa ignore
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa ignore
    },
]

LANGUAGE_CODE = 'tr'
LANGUAGES = [
    ('en', 'English'),
    ('tr', 'Türkçe'),
    ('de', 'Deutsch'),
    ('ru', 'Русский')
]
MODELTRANSLATION_LANGUAGES = [i[0] for i in LANGUAGES]

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
