import os
from decouple import config, Csv

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
SECRET_KEY = config("SECRET_KEY", default='unsafe-secret-key')
DEBUG = config("DEBUG", cast=bool, default=True)

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mistnex.co.zw']
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())



# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'home.apps.HomeConfig',
    'pages.apps.PagesConfig',
    'invoice.apps.InvoiceConfig',
    'facebook_onboarding.apps.FacebookOnboardingConfig',

]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL config
ROOT_URLCONF = 'core.urls'

# Templates
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

# WSGI
WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Email settings (from .env file)
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS & CSRF
CORS_ORIGIN_WHITELIST = [
    'https://mist.pythonanywhere.com',
    'http://ultimatecreative.co.zw',
    'https://ultimatecreative.co.zw',
]
CSRF_TRUSTED_ORIGINS = [
    'https://mist.pythonanywhere.com',
    'https://ultimatecreative.co.zw',
    'http://ultimatecreative.co.zw',
]

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN")

FB_APP_ID = config("FB_APP_ID")
FB_GRAPH_API_VERSION = config("FB_GRAPH_API_VERSION")
FB_CONFIG_ID = config("FB_CONFIG_ID")
FB_FEATURE_TYPE = config("FB_FEATURE_TYPE")
FB_APP_SECRET = config("FB_APP_SECRET")
FB_REDIRECT_URI = config("FB_REDIRECT_URI")
APP_SECRET = config("APP_SECRET")