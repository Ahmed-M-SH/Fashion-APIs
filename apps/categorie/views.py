
from rest_framework.views import APIView, Request, Response

from apps.models import Category
from .serializers import CategorySerializer

# Create your views here.


class CategoryView(APIView):
    serializer_class = CategorySerializer

    def get(self, request: Request):

        data = Category.objects.filter(parent=None)
        ser = self.serializer_class(instance=data, many=True,)
        return Response({
            'data': ser.data
        })
