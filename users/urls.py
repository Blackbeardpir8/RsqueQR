from django.urls import path
from users import views
from users.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path("profile/", profile, name="view-profile"),  # View Profile
    path("register/", register, name="register"),  
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # User Profile Update Route
    path("update-profile/", update_profile, name="update-profile"),  # Update Profile

    # API Endpoints
    path('users/', get_all_users, name='get-all-users'),
    path('users/create/', create_user, name='create-user'),
    path('users/<int:pk>/', get_user, name='get-user'),
    path('users/<int:pk>/update/', update_user, name='update-user'),
    path('users/<int:pk>/delete/', delete_user, name='delete-user'),
]


