from django.urls import path, include
from . import views


urlpatterns = [
    path('orders/', include('apps.orders.urls')),
    path('products/', include('apps.products.urls')),

]
