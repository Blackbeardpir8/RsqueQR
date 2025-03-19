from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.contrib import messages
from django.shortcuts import render

from users.forms import UserForm  # Create a Django Form

# Home Page - List All Users
def index(request):
    users = User.objects.all()
    return render(request, "users/index.html", {"users": users})

# User Creation Form
def user_create_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect("index")
    else:
        form = UserForm()

    return render(request, "users/create.html", {"form": form})



# Get All Users
@api_view(['GET'])
def get_all_users(request):
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

# Create a New User
@api_view(['POST'])
def create_user(request):
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

# Get a Single User
@api_view(['GET'])
def get_user(request, pk):
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

# Update a User (PUT - Full Update)
@api_view(['PUT'])
def update_user(request, pk):
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

# Partially Update a User (PATCH - Partial Update)
@api_view(['PATCH'])
def partial_update_user(request, pk):
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

# Delete a User
@api_view(['DELETE'])
def delete_user(request, pk):
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
