from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-(96x9=9k2(u4kw)y#8=e3%nohkgxp*ab#ilrl@s$h_)j0f^v1f'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
    'control.apps.ControlConfig'
]

MIDDLEWARE = [
    # ! Django Hosts = True
    # 'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ! Django Hosts = True
    # 'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
# ?       'NAME': '',
# ?       'USER': '',
#         'PASSWORD': '1234',
# ?        'HOST': '',
#          'PORT': '5432',
#     }
# }

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'

STATIC_URL = 'static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    BASE_DIR / "core/static"
]



# ? Hosts
# ROOT_HOSTCONF = 'core.hosts'
# DEFAULT_HOST = 'www'

# ? Dramatiq with Redis
# DRAMATIQ_BROKER = {
#     "BROKER": "dramatiq.brokers.redis.RedisBroker",
#     "OPTIONS": {
#         "url": "redis://localhost:6379",
#     },
#     "MIDDLEWARE": [
#         "dramatiq.middleware.Prometheus",
#         "dramatiq.middleware.AgeLimit",
#         "dramatiq.middleware.TimeLimit",
#         "dramatiq.middleware.Callbacks",
#         "dramatiq.middleware.Retries",
#         "django_dramatiq.middleware.DbConnectionsMiddleware",
#         "django_dramatiq.middleware.AdminMiddleware",
#     ]
# }


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'