from multiprocessing import get_context
from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from rest_framework.decorators import api_view, action
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

    def get_serializer_context(self):
        return {'user': self.request.user} if self.request.user.is_authenticated else {}
