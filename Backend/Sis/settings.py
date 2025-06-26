import os
from datetime import timedelta
from decouple import config,Csv
from pathlib import Path
from django.contrib.messages import constants
import mimetypes 
mimetypes.add_type("text/css", ".css", True)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=True, cast=bool)

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000/",
        "http://127.0.0.1:8000/",
        "http://localhost:5173/",
        "http://127.0.0.1:5173/"
    ]


ALLOWED_HOSTS =['*']

USE_L10N = False

DATE_FORMAT = "d-m-Y"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'simple_history',
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
  #  'django_sonar',
    'compressor',
    'debug_toolbar',
    'elasticapm.contrib.django',
    'Autenticacao',
    'Core',
]

SHARED_APPS = [
    'django_tenants', 
    'Cliente',
        'django.contrib.admin',
        'django.contrib.auth',
        'simple_history',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'elasticapm.contrib.django',
        'debug_toolbar',
        'Autenticacao',
        'Core',
        'compressor',
]

TENANT_APPS = [
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'debug_toolbar',
    'simple_history',
    'elasticapm.contrib.django',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    # tenant-specific apps
     'Core',
     'Autenticacao',
     'compressor',
]
INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'Sis.middleware.TenantActiveMiddleware',
    'elasticapm.contrib.django.middleware.TracingMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    "corsheaders.middleware.CorsMiddleware",
   #   'django_sonar.middlewares.requests.RequestsMiddleware',
]

ROOT_URLCONF = 'Sis.urls'

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
                'elasticapm.contrib.django.context_processors.rum_tracing',
            ],
        'libraries':{
            'filters':'Core.templates.filters'
        }
        },
    },
]

WSGI_APPLICATION = 'Sis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

AUTH_USER_MODEL= "Autenticacao.USUARIO"


DATABASES = {
    'default': {
       'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('BANCO'),
        'USER': config('BANCO_USER'),
        'PASSWORD': config('BANCO_PASSWORD'),
        'HOST': config('BANCO_HOST'),
        'PORT': '5432',
        'CONN_MAX_AGE': 500,
        'MAX_CONNS': 20,
        'OPTIONS': {
      #      'sslmode': 'require',
        },
    }
}

SESSION_COOKIE_AGE=604800 # 1 semana

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

#SESSION_ENGINE = 'django.contrib.sessions.backends.file'
#SESSION_FILE_PATH = os.path.join(BASE_DIR,'tmp/')


DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
 )

TENANT_LIMIT_SET_CALLS = True


TENANT_MODEL = "Cliente.Cliente"

TENANT_DOMAIN_MODEL = "Cliente.Domain"

TENANT_COLOR_ADMIN_APPS = False



ELASTIC_APM = {
    'SERVICE_NAME': 'Sis-Otica',  # Nome do seu serviço
    'SECRET_TOKEN': 'qweqW',               # Token secreto, se configurado
    'SERVER_URL': 'http://localhost:8200',
    'ENVIRONMENT': 'production'
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'elasticapm': {
            'level': 'WARNING',
            'class': 'elasticapm.contrib.django.handlers.LoggingHandler',
        },

    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['elasticapm'],
            'propagate': True,
        },
        'MyApp': {
            'level': 'WARNING',
            'handlers': ['elasticapm'],
            'propagate': True,
        },
     
        'elasticapm.errors': {
            'level': 'ERROR',
            'handlers': ['elasticapm'],
            'propagate': True,
        },
    },
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, 'tmp/django_cache'),
        "TIMEOUT": 60,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}

REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
        'DEFAULT_PERMISSION_CLASSES': [
            #'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 25
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "complexsigningkey",  # generate a key and replace me
    "ALGORITHM": "HS512",
}


#CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.redis.RedisCache",
#        "LOCATION": 'redis://191.252.210.233:6379/0',
#	    "TIMEOUT": 60,
#   }
#}
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_AGE=604800 # 1 semana
#SESSION_COOKIE_SECURE = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
    
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)
STATIC_ROOT = os.path.join('static')

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#DJANGO_SONAR = {
#    'excludes': [
#        STATIC_URL,
#        MEDIA_URL,
#        '/sonar/',
#        '/admin/',
#        '/__reload__/',
#    ],
#}



MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
    constants.WARNING: 'alert-warning',
}

UNIDADE=config('UNIDADE')
NOME=config('NOME')


DEFAULT_FROM_EMAIL=config('EMAIL_HOST_USER')
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER= config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD= config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=True
EMAIL_PORT =587
EMAIL_HOST='smtp.office365.com'


CORS_ALLOWED_ORIGINS : True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

X_FRAME_OPTIONS = 'DENY'

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

