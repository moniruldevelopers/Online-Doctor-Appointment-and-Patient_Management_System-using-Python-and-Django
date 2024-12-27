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



class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['user', 'department', 'full_name', 'image', 'specialization', 'phone_number', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter user queryset to show only superusers or staff users
        self.fields['user'].queryset = User.objects.filter(is_superuser=True) | User.objects.filter(is_staff=True)

        # Exclude users who already have a DoctorProfile
        existing_users = DoctorProfile.objects.values_list('user', flat=True)
        self.fields['user'].queryset = self.fields['user'].queryset.exclude(id__in=existing_users)


class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['user', 'department', 'full_name', 'specialization', 'phone_number', 'is_active', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable the 'user' field, but don't render the 'username' field in the template
        if self.instance and self.instance.user:
            self.fields['user'].disabled = True



from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']