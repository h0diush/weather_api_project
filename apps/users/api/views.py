from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenSerializer, UserCreateSerializer, \
    UserUpdateSerializer
from ..models import TokenTelegramBot, User


class UserView(UserViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return super(UserView, self).get_serializer_class()

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def generate_token_for_tgbot(self, request):
        token, created = TokenTelegramBot.objects.get_or_create(
            user=request.user)
        if created:
            token.save()

            return Response(
                {
                    f'message': f'Код сгенерирован {token.code}, '
                                f'далее необходимо перейти в '
                                f'тг бот и отправить код'
                }
            )

        token.delete()
        return Response({'message': 'Код успешно удален'})


class TokenCreateView(TokenObtainPairView):
    serializer_class = TokenSerializer
