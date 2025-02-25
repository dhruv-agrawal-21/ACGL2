from django import forms
from .models import VendorPersonalDetails

class VendorPersonalDetailsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Password")  # User enters 'password', not 'password_hash'

    class Meta:
        model = VendorPersonalDetails
        fields = [
            'vendor_name', 'email', 'phonenumber', 'business_since', 
            'nature_of_services', 'status', 'address', 'state', 'city', 
            'pin_code', 'username', 'password'  # Use 'password' instead of 'password_hash'
        ]
        widgets = {
            'business_since': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),  # Use 'password' instead of 'password_hash'
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalnum():
            raise forms.ValidationError("Only letters and numbers are allowed in the username.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")  # Ensure we validate 'password'
        if (not any(char.isupper() for char in password) or
                not any(char.islower() for char in password) or
                not any(char in "!@#$%^&*()-_=+" for char in password)):
            raise forms.ValidationError("Password must contain an uppercase letter, a lowercase letter, and a special character.")
        return password
    
