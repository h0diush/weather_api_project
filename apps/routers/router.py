from rest_framework.routers import DefaultRouter
from apps.users.api.views import UserView, TokenCreateView

router = DefaultRouter()

router.register('users', UserView)

urlpatterns = [] + router.urls
