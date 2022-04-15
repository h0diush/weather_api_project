from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users.api.views import TokenCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth', TokenCreateView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(),
         name='token_refresh'),
    path('api/', include('apps.routers.router')),
]
