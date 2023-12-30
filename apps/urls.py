from django.urls import path, include
from .views import generate_pdf

urlpatterns = [
    path('', include('apps.API.urls')),
    path('generate-pdf/<int:order_id>/', generate_pdf, name='generate_pdf'),
    path('auth/', include('apps.authentication.urls')),
    path('favorite/', include('apps.favorite.urls')),
    path('user/', include('apps.user.urls')),
    path('categorie', include('apps.categorie.urls'))

    # path('')
]
