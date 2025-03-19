from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer
from .forms import UserRegistrationForm, UserLoginForm, UserForm

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

def user_create_view(request):
    """Render the user creation form and handle form submissions."""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect("index")
    else:
        form = UserForm()
    return render(request, "users/create.html", {"form": form})

# -------------------------------------------------------------------
#                           API Views
# -------------------------------------------------------------------

@api_view(['GET'])
def get_all_users(request):
    """API to get all users."""
    users = User.objects.all()
    if not users.exists():
        return Response({
            "status": False,
            "message": "No users found",
            "data": []
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(users, many=True)
    return Response({
        "status": True,
        "message": "All users fetched",
        "data": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user(request):
    """API to create a new user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": True,
            "message": "User created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "status": False,
        "message": "User creation failed",
        "error": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request, pk):
    """API to get a single user."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({
            "status": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response({
        "status": True,
        "message": "User retrieved successfully",
        "data": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user(request, pk):
    """API to update a user (full update)."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({
            "status": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": True,
            "message": "User updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        "status": False,
        "message": "User update failed",
        "error": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def partial_update_user(request, pk):
    """API to partially update a user."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({
            "status": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": True,
            "message": "User partially updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        "status": False,
        "message": "Partial update failed",
        "error": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, pk):
    """API to delete a user."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({
            "status": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({
        "status": True,
        "message": "User deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------
#                       Authentication Views
# -------------------------------------------------------------------

def register_view(request):
    """User registration view."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Set email as username
            user.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
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
