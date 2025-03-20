from django.contrib import admin
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    ordering = ('phone_number',)
    list_filter = ('is_staff', 'is_superuser', 'date_joined')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'middle_name', 'age', 'gender', 'blood_type', 
        'primary_doctor_name', 'primary_doctor_contact', 
        'emergency_contact', 'emergency_contact_phone', 'emergency_relation'
    )
    search_fields = (
        'user__first_name', 'user__last_name', 'user__email', 
        'primary_doctor_name', 'primary_doctor_contact', 
        'emergency_contact__user__first_name', 'emergency_contact__user__last_name', 
        'emergency_contact_phone'
    )
    list_filter = ('gender', 'blood_type', 'emergency_relation')

    fieldsets = (
        ("User Info", {
            "fields": ("user", "middle_name", "age", "gender", "address", "profile_picture")
        }),
        ("Medical Information", {
            "fields": ("medical_conditions", "allergies", "insurance_documents")
        }),
        ("Emergency Contact", {
            "fields": ("emergency_contact", "emergency_contact_phone", "emergency_relation")
        }),
        ("Doctor Info", {
            "fields": ("primary_doctor_name", "primary_doctor_contact")
        }),
    )
