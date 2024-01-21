from django.urls import path, include
from .views import generate_file_app, generate_pdf

urlpatterns = [
    path('', include('apps.API.urls')),
    path('generate-pdf/<int:order_id>/', generate_pdf, name='generate_pdf'),
    # path('generate-app-file/', generate_file_app, name='generate_app'),
    path('auth/', include('apps.authentication.urls')),
    path('favorite/', include('apps.favorite.urls')),
    path('user/', include('apps.user.urls')),
    path('categorys/', include('apps.categorie.urls')),
    path('orders/', include('apps.orders.urls')),

    # path('')
]
