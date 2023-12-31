from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from ..pagination import StandardResultsSetPagination

from apps.models import Order, Product
from . import serializers

# Create your views here.


class OrderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    queryset = Order.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.OrderSerializers

    def get_serializer_context(self):
        return {'user': self.request.user} if self.request.user.is_authenticated else {}


class ProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.SingleProductSerializer
        else:
            return serializers.ProductSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        return {'user': self.request.user} if self.request.user.is_authenticated else {}
