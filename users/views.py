from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm, UserForm



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


@login_required
def user_create_view(request):
    """Render user form with logged-in user data (non-editable)."""
    
    # Pre-fill form with logged-in user data
    initial_data = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "phone_number": request.user.phone_number,
    }

    form = UserForm(initial=initial_data)  # Pass data to form (Read-Only)
    
    return render(request, "users/create_user.html", {"form": form})

@login_required
def profile(request):
    """Display the user's profile details"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    return render(request, "users/profile.html", {"profile": user_profile})


@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.save()
            form.save()
            return redirect("home")
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    return render(request, "users/update_profile.html", {"form": form})


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
    """User registration view."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Create an empty UserProfile
            login(request, user)
            return redirect("home")  # Redirect to home page
    else:
        form = UserRegistrationForm()
    
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """User login view."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")  # Email field
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.first_name}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

