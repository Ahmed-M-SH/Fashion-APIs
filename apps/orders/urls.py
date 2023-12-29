from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.OrderView.as_view({'get': 'list'})),
    path('<pk>/', views.OrderView.as_view({'get': 'retrieve'})),
]
