from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseForbidden

from users.models import User
from users.serializers import UserSerializer
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.models import UserProfile
from users.forms import UserRegistrationForm, UserProfileForm



# -------------------------------------------------------------------
#                           Template Views
# -------------------------------------------------------------------

def home_view(request):
    """Render the home page."""
    return render(request, 'home.html')


def index(request):
    """List all users on the index page."""
    users = User.objects.all()
    return render(request, "users/index.html", {"users": users})

def how_it_works_view(request):
    return render(request, "users/how_it_works.html")

def terms_of_service(request):
    return render(request, "users/terms_of_service.html")

def privacy_policy(request):
    return render(request, "users/privacy_policy.html")


@login_required
def user_details_view(request):
    """Render user details form with pre-filled non-editable fields."""

    # Fetch or create the user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to profile after updating
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    return render(request, "users/user_details.html", {"form": form})

@login_required
def profile(request):
    """Display the user's profile details (View-Only)"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    return render(request, "users/view_profile.html", {"profile": user_profile})


@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            if form.instance.user != request.user:
                return HttpResponseForbidden("You are not allowed to edit this profile.")  # Prevent editing others' profiles
            
            form.save()
            return redirect("view-profile")  # Redirect to View Profile after updating
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    return render(request, "users/update_profile.html", {"form": form})


@login_required
def dashboard(request):
    role = request.user.role  # Assuming `role` is stored in the User model
    return render(request, "users/dashboard.html", {"role": role})

# -------------------------------------------------------------------
#                           API Views
# -------------------------------------------------------------------

@api_view(['GET'])
def get_all_users(request):
    """API to fetch all users."""
    users = User.objects.all()
    if not users.exists():
        return Response({"status": False, "message": "No users found", "data": []}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(users, many=True)
    return Response({"status": True, "message": "All users fetched", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    """API to create a new user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True, "message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    return Response({"status": False, "message": "User creation failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user(request, pk):
    """Retrieve a specific user's details including profile"""
    try:
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(user=user)
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "middle_name": profile.middle_name,
            "age": profile.age,
            "address": profile.address,
            "gender": profile.gender,
            "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
            "medical_conditions": profile.medical_conditions,
            "allergies": profile.allergies,
            "blood_type": profile.blood_type,
            "primary_doctor_name": profile.primary_doctor_name,
            "primary_doctor_contact": profile.primary_doctor_contact,
            "emergency_contact": profile.emergency_contact.user.email if profile.emergency_contact else None,
            "emergency_relation": profile.emergency_relation,
        }
        return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        return Response({"status": False, "message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_user(request, pk):
    """API to fully update a user."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True, "message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    return Response({"status": False, "message": "User update failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def partial_update_user(request, pk):
    """API to partially update a user."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True, "message": "User partially updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    return Response({"status": False, "message": "Partial update failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, pk):
    """API to delete a user."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"status": True, "message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------
#                       Authentication Views
# -------------------------------------------------------------------


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]

        user = User.objects.create_user(
            email=email, 
            password=password, 
            role=role, 
            first_name=first_name, 
            last_name=last_name, 
            phone_number=phone_number
        )
        user.save()
        login(request, user)

        return redirect("dashboard")  # Redirect based on role

    return render(request, "users/register.html")




def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "users/login.html")


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")




from rest_framework import generics, permissions
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
# List & Create Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Retrieve, Update & Delete User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# User Profile Detail & Update
class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsDoctor, IsUser

class AdminOnlyView(APIView):
    """Only Admins can access this view"""
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome, Admin!"})


class DoctorOnlyView(APIView):
    """Only Doctors can access this view"""
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        return Response({"message": "Welcome, Doctor!"})


class UserOnlyView(APIView):
    """Only Regular Users can access this view"""
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({"message": "Welcome, User!"})

from django.contrib.auth.decorators import login_required
from .decorators import role_required

@login_required
@role_required(["Admin"])  # Only Admins can access this
def admin_dashboard(request):
    return render(request, "users/admin_dashboard.html")

@login_required
@role_required(["Doctor"])  # Only Doctors can access this
def doctor_dashboard(request):
    return render(request, "users/doctor_dashboard.html")

@login_required
@role_required(["User"])  # Only Users can access this
def user_dashboard(request):
    return render(request, "users/user_dashboard.html")