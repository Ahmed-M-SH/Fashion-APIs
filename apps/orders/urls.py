from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.OrderView.as_view({'get': 'list'})),
    path('create/', views.OrderView.as_view({'post': 'create'})),
    path('payment-detail/',
         views.OrderView.as_view({'get': 'get_payment_details'})),
    path('<pk>/', views.OrderView.as_view({'get': 'retrieve'})),
    path('<pk>/update/',
         views.OrderView.as_view({'put': 'partial_update', 'patch': 'partial_update'})),
]
# {'put': 'partial_update', 'patch': 'partial_update'}
