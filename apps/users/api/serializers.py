from rest_framework import serializers

from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from config.settings.development import BOT, TG_ID
from ..validators import validate_phone as vd
from .utilits import get_temperature as temperature_in_city


class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(help_text='Введите последние 9 цифр',
                                  label='Телефон')

    class Meta:
        model = User
        fields = (
            'email', 'username', 'phone', 'last_name', 'first_name', 'surname',
            'password', 'city'
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            surname=validated_data['surname'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def validate_phone(value):
        return vd(value)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone', 'is_active')


class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    temperature = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'phone', 'username', 'full_name', 'city',
            'temperature', 'country'
        )

    @staticmethod
    def _get_temperature_and_country(city):
        TEMP, COUNTRY = temperature_in_city(city)
        BOT.send_message(chat_id=431749676, text='hello')
        return {'temp': TEMP, 'country': COUNTRY}

    @staticmethod
    def get_full_name(obj):
        full_name = f'{obj.last_name} {obj.first_name} {obj.surname}'
        return full_name

    def get_temperature(self, obj):
        return f'{self._get_temperature_and_country(obj.city)["temp"]} °C'

    def get_country(self, obj):
        return f'{self._get_temperature_and_country(obj.city)["country"]}'


class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(help_text='Введите последние 9 цифр',
                                  label='Телефон')

    class Meta:
        model = User
        fields = (
            'email', 'phone', 'username', 'last_name', 'first_name', 'surname',
            'city',
        )

    @staticmethod
    def validate_phone(value):
        return vd(value)


class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        token['email'] = user.email
        token['city'] = user.city
        token['created'] = f'{user.date_joined.strftime("%H:%M  %d.%b.%Y")}'

        return token
