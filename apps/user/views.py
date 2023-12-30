from rest_framework.permissions import IsAuthenticated
from apps.models import User
from .serializer import UpdateUserSerializer, UserProfileSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
# Create your views here.
# start User Using calss BaseViewsets


class UserViewsets(viewsets.ModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateUserSerializer
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(is_deleted=False, is_active=True)


class UpdateUserViewsets(viewsets.ModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(
    #         instance=request.user, data=request.data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response({
    #             'data': 'User Updated Suscceful',
    #             'user': serializer.data
    #         }, status=200)
    #     else:
    #         return Response({
    #             'error': serializer.errors
    #         }, status=404)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'data': 'User Updated Suscceful',
                'user': serializer.data
            }, status=200)
        else:
            return Response({
                'error': serializer.errors
            }, status=404)

    def get_queryset(self):

        return User.objects.filter(is_deleted=False, is_active=True)


class UserProfileViewset(viewsets.ModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    def get_queryset(self):
        return User.objects.filter(is_deleted=False, is_active=True, id=self.request.user.id)

# End User Using calss BaseViewsets
