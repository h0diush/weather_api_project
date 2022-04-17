# import logging.config
from datetime import timedelta

import environ
# from django.utils.log import DEFAULT_LOGGING
from telegram import Bot

from config.settings.base import *

environ.Env.read_env(env_file=".env")
env = environ.Env(DEBUG=(bool, False))

DEBUG = env('DEBUG')
TG_ID = env('TG_ID')
TOKEN_BOT = env('TOKEN_BOT')
BOT = Bot(token=TOKEN_BOT)
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

APPID_OPENWEATHERMAP = env('APPID_OPENWEATHERMAP')

CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    'send_message_in_telegram': {
        'task': 'apps.users.tasks.get_send_message',
        'schedule': 10800.0
    }
}

SECRET_KEY = env('SECRET_KEY')

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    # 'django_filters',
    # 'drf_spectacular',
]

LOCAL_APPS = [
    "apps.weather.apps.WeatherConfig",
    "apps.users.apps.UsersConfig"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DJOSER = {
    'HIDE_USERS': False,
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        # 'user_create': 'apps.users.api.serializers.UserCreateSerializer',
        'user': 'apps.users.api.serializers.UserListSerializer',
        'current_user': 'apps.users.api.serializers.CurrentUserSerializer',
        # 'user_list': 'apps.users.api.serializers.UserListSerializer',
    },
    'PERMISSIONS': {
        'activation': ['rest_framework.permissions.AllowAny'],
        'password_reset': ['rest_framework.permissions.AllowAny'],
        'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_password': ['djoser.permissions.CurrentUserOrAdmin'],
        'username_reset': ['rest_framework.permissions.AllowAny'],
        'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_username': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_delete': ['djoser.permissions.CurrentUserOrAdmin'],
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    }

}

# logger = logging.getLogger(__name__)
#
# LOG_LEVEL = "DEBUG"
# logging.config.dictConfig(
#     {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "console": {
#                 "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
#             },
#             "file": {
#                 "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
#             "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
#         },
#         "handlers": {
#             "console": {
#                 "class": "logging.StreamHandler",
#                 "formatter": "console",
#             },
#             "file": {
#                 "level": "DEBUG",
#                 "class": "logging.FileHandler",
#                 "formatter": "file",
#                 "filename": "blog-debug.log",
#             },
#             "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
#         },
#         "loggers": {
#             "": {"level": "DEBUG", "handlers": ["console", "file"],
#                  "propagate": False},
#             "apps": {
#                 "level": "DEBUG",
#                 "handlers": ["console"],
#                 "propagate": False,
#             },
#             "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
#         },
#     }
# )
