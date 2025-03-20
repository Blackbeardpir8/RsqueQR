from django.urls import path
from users import views
from users.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path("create/", user_create_view, name="user_create"),
    path("register/", register, name="register"),  
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # User Profile Update Route
    path("profile/",profile, name = "profile"),
    path("update_profile/", update_profile, name="update-profile"),

    # API Endpoints
    path('users/', get_all_users, name='get-all-users'),
    path('users/create/', create_user, name='create-user'),
    path('users/<int:pk>/', get_user, name='get-user'),
    path('users/<int:pk>/update/', update_user, name='update-user'),
    path('users/<int:pk>/delete/', delete_user, name='delete-user'),
]

