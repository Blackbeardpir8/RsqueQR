from django.urls import path
from users import views
from users.views import *

urlpatterns = [
    path('', views.home_view, name='home'),
    path("create/", user_create_view, name="user_create"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),


    path('users/', get_all_users, name='get-all-users'),  # GET all users
    path('users/create/', create_user, name='create-user'),  # POST new user
    path('users/<int:pk>/', get_user, name='get-user'),  # GET single user
    path('users/<int:pk>/update/', update_user, name='update-user'),  # PUT update user
    path('users/<int:pk>/partial-update/', partial_update_user, name='partial-update-user'),  # PATCH partial update
    path('users/<int:pk>/delete/', delete_user, name='delete-user'),  # DELETE user
]

