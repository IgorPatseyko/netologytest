from django.db.models import Q
from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров


    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    # filterset_fields = ['creator', ]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated() and IsOwnerOrReadOnly()]
        return []

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Advertisement.objects.filter(creator=self.request.user, draft=True) | Advertisement.objects.filter(draft=False)
        else:
            return Advertisement.objects.filter(draft=False)

    @action(detail=True, methods=['get'])
    def mark_favourite(self, request):
        adv = self.get_object()
        if adv.creator == self.request.user:
            return Response({'status': 'you cant mark your own ads'})
        else:
            adv.favourite.add(self.request.user)
            adv.save()
            return Response({'status': f'adv #{adv.id} marked as favourite'})
