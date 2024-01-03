from django.urls import path, include
from . import views

urlpatterns = [
    # User Method
    # path('', views.UserViews.as_view()),
    # path('create/', views.CreateUserView.as_view()),
    # # -> for Customer
    # # path('gender/', views.gender_get), # -> for Gender
    # path("profile/",
    #      views.UserViewsets.as_view({'get': 'profile'}), name="profile"),
    # path('<int:pk>/', views.UserViews.as_view()),
    # path('<int:pk>/update/', views.UserUpdateView.as_view()),
    # path('<int:pk>/delete/', views.UserDeleteView.as_view()),

    # ================================
    path('cart/', include("apps.cart.urls")),
    path('create/', views.UserViewsets.as_view({'post': 'create'})),
    path("profile/",
         views.UserProfileViewset.as_view({'get': 'list'}), name="profile"),
    path('<int:pk>/', views.UserViewsets.as_view({'get': 'retrieve'})),

    path('profile/update/',
         views.UpdateUserViewsets.as_view({'put': 'partial_update', 'patch': 'partial_update'})),

    path('<int:pk>/delete/',
         views.UserViewsets.as_view({'delete': 'destroy'})),
    # ======================================



    # User address
    # path('<user_id>/address/',views.User_address_get),
    # path('<user_id>/address/create/', views.user_address_post),
    # path('<user_id>/address/<pk>/update/', views.user_address_update),
    # path('<user_id>/address/<pk>/delete/', views.user_address_delete),

    # User Gender
    # path('<int:user_id>/gender/',views.gender_get),
    # path('<int:user_id>/gender/update/', view=views.gender_update),


    # User Profile
    # path('<user_id>/profile/',views.profile_get),
    # path('<user_id>/profile/update/',views.profile_update),
]
