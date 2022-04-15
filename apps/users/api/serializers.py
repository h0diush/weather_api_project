from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..validators import validate_phone as vd


class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(help_text='Введите последние 9 цифр',
                                  label='Телефон')

    class Meta:
        model = User
        fields = (
            'email', 'username', 'phone', 'last_name', 'first_name', 'surname',
            'password'
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

    def validate_phone(self, value):
        return vd(value)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone', 'is_active')


class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'username', 'full_name')

    def get_full_name(self, obj):
        full_name = f'{obj.last_name} {obj.first_name} {obj.surname}'
        return full_name


class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(help_text='Введите последние 9 цифр',
                                  label='Телефон')

    class Meta:
        model = User
        fields = (
            'email', 'phone', 'username', 'last_name', 'first_name', 'surname',
        )


class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        token['email'] = user.email
        token['created'] = f'{user.date_joined.strftime("%H:%M  %d.%b.%Y")}'

        return token
