from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters

from apps.cart.serializers import CreateFavoriteSerializers
from ..pagination import StandardResultsSetPagination
from rest_framework.views import Response

from apps.models import Favorite, Product, Review, Review_Likes
from . import serializers

# Create your views here.


class FavoriteView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # serializer_class = serializers.FavoriteSerializers
    lookup_field = 'product_id'

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateFavoriteSerializers
        else:
            return serializers.FavoriteSerializers

    def create(self, request, *args, **kwargs):
        ser = CreateFavoriteSerializers(
            data=request.data, context={'user': request.user})

        # print(
        # f"User: {request.user}, Product ID: {request.data.get('product')}")

        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(status.HTTP_200_OK)

    def get_queryset(self):
        return Favorite.objects.filter(user__id=self.request.user.id).select_related('user', 'product')

    @action(detail=True)
    def destroy_list(self, request, *args, **kwargs):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        item = request.data
        # print(item)
        user = request.user
        if item:
            try:
                # print(list(item))
                for id in item:
                    # print(id.get('product_id'))
                    Favorite.objects.filter(
                        user_id=request.user.id, id=id.get('id')).delete()
                return Response({
                    'data': 'Done'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f'error {e}'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # user.favorites.all().delete()
            return Response(status=status.HTTP_200_OK)
