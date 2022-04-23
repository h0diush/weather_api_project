from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User
from .utilits import get_temperature as temperature_in_city
from ..validators import validate_phone as vd


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
            phone=validated_data['phone'],
            city=validated_data['city']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def validate_phone(value):
        return vd(value)


class UserListSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone', 'is_active')

    @staticmethod
    def get_phone(obj):
        return f'+375{obj.phone}'


class CurrentUserSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
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
    def get_phone(obj):
        return f'+375{obj.phone}'

    @staticmethod
    def get_full_name(obj):
        full_name = f'{obj.last_name} {obj.first_name} {obj.surname}'
        return full_name

    @staticmethod
    def get_temperature(obj):
        return f'{temperature_in_city(obj.city)["temperature"]} °C'

    @staticmethod
    def get_country(obj):
        return f'{temperature_in_city(obj.city)["country"]}'


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
