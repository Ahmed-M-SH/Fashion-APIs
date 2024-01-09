from rest_framework.views import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from ..pagination import StandardResultsSetPagination
from rest_framework.decorators import action


from apps.models import City, Currency, Order, Payment_type, Product
from . import serializers

# Create your views here.


class OrderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    queryset = Order.objects.all()
    # pagination_class = StandardResultsSetPagination
    serializer_class = serializers.OrderSerializers

    def get_serializer_context(self):
        return {'user': self.request.user} if self.request.user.is_authenticated else {}

    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def get_payment_details(self, request, *args, **kwargs):
        currency = Currency.objects.filter(is_active=True)
        currencySer = serializers.CurrencySerializers(
            instance=currency, many=True)
        city = City.objects.filter(is_active=True)
        citySer = serializers.CitySerializers(
            instance=city, many=True)
        payment_type = Payment_type.objects.filter(is_active=True)
        paymentser = serializers.Payment_TypeSerializers(
            instance=payment_type, many=True)
        return Response({
            'currency': currencySer.data,
            'city': citySer.data,
            'payment_type': paymentser.data
        })
