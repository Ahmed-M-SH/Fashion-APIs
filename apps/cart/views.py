from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from ..pagination import StandardResultsSetPagination
from rest_framework.views import Response

from apps.models import Favorite, Product, Review, Review_Likes
from . import serializers


class CartView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FavoriteSerializers
    lookup_field = 'product_id'

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateFavoriteSerializers
        else:
            return serializers.FavoriteSerializers

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
