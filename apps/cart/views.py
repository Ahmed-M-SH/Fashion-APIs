from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from ..pagination import StandardResultsSetPagination
from rest_framework.views import Response
from rest_framework.decorators import action

from apps.models import Cart, Favorite, Product, Review, Review_Likes, User
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


# s = Store.objects.filter(product_store__Product_Cart__user__id=20)


# class CartViewsets(viewsets.ModelViewSet):
#     """
#     ``New Way``
#     add numpy array and use Viewsetes

#     Args:
#         viewsets (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     serializer_class = serializers.CartViewSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Cart.objects.all()
#     filter_backends = [filters.OrderingFilter, filters.SearchFilter]
#     ordering_fields = '__all__'

    # def list(self, request, *args, **kwargs):
    #     """_summary_

    #     Args:
    #         request (_type_): _description_

    #     Returns:
    #         _type_: _description_
    #     """
    #     store = Store.objects.filter(
    #         product__product_item__item_Cart__user_id=request.user.id).annotate(count=Count('id'))
    #     stors = {}
    #     for s in store:
    #         products = {
    #             'id': s.id,
    #             'store_name': s.store_name,
    #         }
    #         p = np.array(Product_item.objects.filter(
    #             item_Cart__user__id=request.user.id, product__store=s))
    #         products['product'] = np.array(self.serializer_class(instance=p, many=True, context={
    #             'user': request.user
    #         }).data)
    #         stors[str(s.store_name)] = products
    #         return Response({
    #             'data': np.array(stors.values()).tolist()
    #         })


class CartMethodViewsetes(viewsets.ModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs):
        """_summary_
        Args:
            request (_type_): _description_
        Returns:
            _type_: _description_
        """
        user = self.request.user
        user: User
        ser = self.serializer_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            data = user.add_cart(**ser.validated_data)
            # ser.save(user_id=request.user.id)
            return Response({
                'data': 'Added Or Updated to Cart done'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': ser.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.create(request=request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def create_list(self, request, *args, **kwargs):
        """_summary_
        Args:
            request (Request): _description_
        Returns:
            _type_: _description_
        """
        ser = self.serializer_class(
            data=request.data.get('products' or None), many=True)
        if ser.is_valid(raise_exception=True):
            ser.save(user_id=request.user.id)
            return Response({
                'data': 'Added to Cart done'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': ser.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def destroy_list(self, request, *args, **kwargs):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        item = request.data.get('products' or None)
        if item:
            try:
                # print(list(item))
                for id in item:
                    # print(id.get('product_id'))
                    Cart.objects.filter(
                        user_id=request.user.id, product_id=id.get('product_id')).delete()
                return Response({
                    'data': 'Done'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f'error {e}'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'error in data'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def update_list(self, request, *args, **kwargs):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        ser = self.serializer_class(
            data=request.data.get('products' or None), many=True)
        if ser.is_valid(raise_exception=True):
            ser.save(user_id=request.user.id)
            return Response({
                'data': 'Added to Cart done'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': ser.errors
            }, status=status.HTTP_400_BAD_REQUEST)
