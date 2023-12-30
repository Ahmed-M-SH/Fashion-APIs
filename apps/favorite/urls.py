from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.FavoriteView.as_view({'get': 'list'})),

    path('create/', views.FavoriteView.as_view({'post': 'create'})),

    path('<product_id>/delete/',
         views.FavoriteView.as_view({'delete': 'destroy'})),

    #     path('review/create/',
    #          views.CreateReviewView.as_view({'post': 'create'})),
    #     path('reviewlike/create/',
    #          views.CreateReviewLikeView.as_view({'post': 'create'})),



    #     path('<pk>/', views.ProductView.as_view({'get': 'retrieve'})),

    # path('products/create/', views.ProductView.as_view({'post': 'create'})),

]
