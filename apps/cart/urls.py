from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CartView.as_view({'get': 'list'}), name='cart'),
    path(
        'add/', views.CartMethodViewsetes.as_view({'post': 'create'}), name='add-cart'),
    path('add-list/',
         views.CartMethodViewsetes.as_view({'post': 'create_list'}), name='add-cart'),
    path('<int:pk>/delete/',
         views.CartMethodViewsetes.as_view({'delete': 'destroy'}), name='delete-cart'),
    path('delete-all/',
         views.CartMethodViewsetes.as_view({'post': 'destroy_list'}), name='delete_all-cart'),
    path('delete-list/', views.CartMethodViewsetes.as_view({'post': 'destroy_list'}),
         name='delete_list-cart'),
    path('<int:pk>/update-count/',
         views.CartMethodViewsetes.as_view({'post': 'create'}), name='update-cart'),
]
