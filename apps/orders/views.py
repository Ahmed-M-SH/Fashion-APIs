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
