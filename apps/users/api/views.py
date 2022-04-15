from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenSerializer, UserCreateSerializer, \
    UserUpdateSerializer
from ..models import User


class UserView(UserViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return super(UserView, self).get_serializer_class()


class TokenCreateView(TokenObtainPairView):
    serializer_class = TokenSerializer
