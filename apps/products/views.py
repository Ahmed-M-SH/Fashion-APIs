from urllib import request
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from ..pagination import StandardResultsSetPagination
from rest_framework.views import Response

from apps.models import Favorite, Product, Promotion, Rate, Review, Review_Likes
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers

# Create your views here.


class ProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'price', 'description',]
    filterset_fields = ['name', 'price', 'category']
    ordering_fields = '__all__'
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SingleProductSerializer
        else:
            return serializers.ProductSerializer

    def get_serializer_context(self):
        return {'user': self.request.user} if self.request.user.is_authenticated else {}


class CreateReviewView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializers
    lookup_field = 'product_id'

    def get_serializer_context(self):
        return {'user': self.request.user}

    def create(self, request, *args, **kwargs):
        # serializers = self.get_serializer_class()
        # serializers(data=request.data)
        serializers = self.serializer_class(
            data=request.data, context={'user': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({
                'data': 'Created Suscceful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': serializers.errors
            }, status=status.HTTP_404_NOT_FOUND)


class CreateRatingView(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = serializers.RateSerializers
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user': self.request.user}

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CreateReviewLikeView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review_Likes.objects.all()
    serializer_class = serializers.ReviewLikeSerializers
    lookup_field = 'review_id'
    # lookup_url_kwarg = ['pk', 'review_id']

    def get_queryset(self):
        if self.action == 'destroy':
            return Review_Likes.objects.filter(user=self.request.user)
        else:
            return Review_Likes.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.action == 'destroy':
            return serializers.DeleteReviewLikeSerializers
        else:
            return serializers.ReviewLikeSerializers

    def create(self, request, *args, **kwargs):

        serializers = self.serializer_class(
            data=request.data, context={'user': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({
                'data': 'Created Suscceful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': serializers.errors
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PromotionView(viewsets.ModelViewSet):
    queryset = Promotion.objects.filter(is_active=True)
    serializer_class = serializers.PromotionSerializers
