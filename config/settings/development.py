import environ

from config.settings.base import *

environ.Env.read_env(env_file=".env")
env = environ.Env(DEBUG=(bool, False))

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

SECRET_KEY = env('SECRET_KEY')

THIRD_PARTY_APPS = [
    # 'rest_framework',
    # 'rest_framework.authtoken',
    # 'rest_framework_simplejwt',
    # 'djoser',
    # 'django_filters',
    # 'drf_spectacular',
]

LOCAL_APPS = [
    "apps.weather.apps.WeatherConfig"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
