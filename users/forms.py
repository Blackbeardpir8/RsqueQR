from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User, UserProfile

# -----------------------------------
# User Registration Form
# -----------------------------------
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

# -----------------------------------
# User Login Form
# -----------------------------------
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        fields = ["username", "password"]

# -----------------------------------
# User Profile Form
# -----------------------------------
class UserProfileForm(forms.ModelForm):
    """Form for updating user profile details while keeping user fields read-only."""

    first_name = forms.CharField(disabled=True, required=False)
    last_name = forms.CharField(disabled=True, required=False)
    email = forms.EmailField(disabled=True, required=False)
    phone_number = forms.CharField(disabled=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            "first_name", "last_name", "email", "phone_number",  # Read-only fields
            "middle_name", "age", "address", "gender", "profile_picture",
            "medical_conditions", "allergies", "insurance_documents",
            "emergency_contact", "emergency_relation", "blood_type",
            "primary_doctor_name", "primary_doctor_contact"
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Get logged-in user
        super().__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["phone_number"].initial = user.phone_number

    def save(self, commit=True):
        """Save profile data without modifying read-only fields."""
        profile = super().save(commit=False)

        # Ensure user fields are not modified
        user = profile.user
        user.first_name = self.cleaned_data.get("first_name", user.first_name)
        user.last_name = self.cleaned_data.get("last_name", user.last_name)
        user.email = self.cleaned_data.get("email", user.email)
        user.phone_number = self.cleaned_data.get("phone_number", user.phone_number)

        if commit:
            user.save()
            profile.save()
        return profile
