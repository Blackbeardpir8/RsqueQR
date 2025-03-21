from django.urls import path
from users import views
from users.views import *

urlpatterns = [
    path('', home_view, name='home'),

    path("how-it-works/", how_it_works_view, name="how_it_works"),
    path("terms-of-service/", terms_of_service, name="terms_of_service"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),


    path("profile/", profile, name="view-profile"),  # View Profile
    path("register/", register, name="register"),  
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),

    # User Profile Update Route
    path("update-profile/", update_profile, name="update-profile"),  # Update Profile

    # API Endpoints
    path('users/', get_all_users, name='get-all-users'),
    path('users/create/', create_user, name='create-user'),
    path('users/<int:pk>/', get_user, name='get-user'),
    path('users/<int:pk>/update/', update_user, name='update-user'),
    path('users/<int:pk>/delete/', delete_user, name='delete-user'),


    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),

    path("admin-only/", AdminOnlyView.as_view(), name="admin-only"),
    path("doctor-only/", DoctorOnlyView.as_view(), name="doctor-only"),
    path("user-only/", UserOnlyView.as_view(), name="user-only"),
]

