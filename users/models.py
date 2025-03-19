from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    RELATIONSHIP_CHOICES = [
        ('Parent', 'Parent'),
        ('Sibling', 'Sibling'),
        ('Spouse', 'Spouse'),
        ('Child', 'Child'),
        ('Friend', 'Friend'),
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

    # Basic User Details
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Contact Information
    phone_number = models.CharField(max_length=15, unique=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    # Medical Information
    medical_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    insurance_documents = models.FileField(upload_to='insurance_docs/', blank=True, null=True)

    # Emergency Contact (Relation to Another User)
    emergency_contact = models.ForeignKey(
        'self',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_for"
    )
    emergency_relation = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES, blank=True, null=True)

    # Extra Fields
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    primary_doctor_name = models.CharField(max_length=100, blank=True, null=True)
    primary_doctor_contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name} - {self.phone_number}"
