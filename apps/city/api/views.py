from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.city.models import City
from .serializers import CityListSerializer


class CityListView(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
