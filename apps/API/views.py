from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.decorators import api_view, action


# Create your views here.


class OrderView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
