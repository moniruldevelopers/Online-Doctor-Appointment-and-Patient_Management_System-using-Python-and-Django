from .models import User
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

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


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['department', 'full_name', 'specialization', 'phone_number', 'image']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['name', 'mobile', 'profile_pic', 'designation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'