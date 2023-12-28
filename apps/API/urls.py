from django.urls import path, include
from . import views


urlpatterns = [
    path('orders/', views.OrderView.as_view({'get': 'list'})),
    path('orders/<pk>/', views.OrderView.as_view({'get': 'retrieve'})),
    path('products/', views.ProductView.as_view({'get': 'list'})),
    path('products/create/', views.ProductView.as_view({'post': 'create'})),

    path('products/<pk>/', views.ProductView.as_view({'get': 'retrieve'})),
    # path('products/create/', views.ProductView.as_view({'post': 'create'})),

]
