from rest_framework.routers import DefaultRouter

from apps.city.api.views import CityListView
from apps.users.api.views import UserView

router = DefaultRouter()

router.register('users', UserView)
router.register('city', CityListView)

urlpatterns = [] + router.urls
