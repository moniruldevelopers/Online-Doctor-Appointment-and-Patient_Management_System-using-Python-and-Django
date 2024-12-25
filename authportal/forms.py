from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm



class CustomSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 15:
            raise ValidationError("Username must be 15 characters or fewer.")
        return username