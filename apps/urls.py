from django.urls import path
from .views import generate_pdf

urlpatterns = [
    path('generate-pdf/<int:order_id>/', generate_pdf, name='generate_pdf'),
]
