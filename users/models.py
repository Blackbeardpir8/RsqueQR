from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, phone_number, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Doctor', 'Doctor'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')

    def is_admin(self):
        return self.role == "Admin"

    def is_doctor(self):
        return self.role == "Doctor"

    def is_user(self):
        return self.role == "User"
    
    username = None  # Remove default username field
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    RELATION_CHOICES = [
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Spouse', 'Spouse'),
        ('Friend', 'Friend'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Relative', 'Relative'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Additional Details
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Medical Information
    medical_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    insurance_documents = models.FileField(upload_to='insurance_docs/', blank=True, null=True)

    # Emergency Contact
    emergency_contact = models.ForeignKey(
        'self',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_for"
    )
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_relation = models.CharField(max_length=10, choices=RELATION_CHOICES, blank=True, null=True)

    # Extra Fields
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    primary_doctor_name = models.CharField(max_length=100, blank=True, null=True)
    primary_doctor_contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.first_name} {self.user.last_name}"

