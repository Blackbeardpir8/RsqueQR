from django.urls import path
from users.views import *

urlpatterns = [
    path('users/', get_all_users, name='get-all-users'),  # GET all users
    path('users/create/', create_user, name='create-user'),  # POST new user
    path('users/<int:pk>/', get_user, name='get-user'),  # GET single user
    path('users/<int:pk>/update/', update_user, name='update-user'),  # PUT update user
    path('users/<int:pk>/partial-update/', partial_update_user, name='partial-update-user'),  # PATCH partial update
    path('users/<int:pk>/delete/', delete_user, name='delete-user'),  # DELETE user
]
