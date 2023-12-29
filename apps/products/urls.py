from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductView.as_view({'get': 'list'})),
    path('create/', views.ProductView.as_view({'post': 'create'})),

    path('<pk>/', views.ProductView.as_view({'get': 'retrieve'})),
    # path('products/create/', views.ProductView.as_view({'post': 'create'})),

]
