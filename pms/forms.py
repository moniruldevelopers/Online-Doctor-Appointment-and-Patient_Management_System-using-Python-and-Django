from .models import User
from django.contrib.auth.models import User
from .models import *
from django import forms

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'full_name', 'date_of_birth', 'gender', 'phone_number',
            'present_address', 'permanent_address', 'city', 'blood_type',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'allergies', 'HIV_positive', 'thalassemia', 'diabetes', 'hypertension', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'form-control is-invalid'})
