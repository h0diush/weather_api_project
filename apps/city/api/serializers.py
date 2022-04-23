from rest_framework import serializers

from apps.city.models import City
from apps.users.models import User


class CityListSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('name', 'country', 'count_users', 'users')

    @staticmethod
    def get_users(obj):
        users: list = User.objects.filter(city=obj.name).values('username',
                                                                'email',
                                                                'phone',
                                                                'city')
        return users
