from .models import User
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.contrib.auth.models import Group






class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = '__all__'
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'color_logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'white_logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'opening_hours':forms.TextInput(attrs={'class': 'form-control'}),
            'site_facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'site_x': forms.URLInput(attrs={'class': 'form-control'}),
            'site_instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'site_pinterest': forms.URLInput(attrs={'class': 'form-control'}),
        }



class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = ['title', 'subtitle', 'image']



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'member_id', 'phone_number', 'image', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'member_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Member ID'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio', 'rows': 4}),
        }



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }







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




class AppointmentForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=PatientProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-placeholder': 'Search Patient ID'}),
        label="Patient ID"
    )
    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-placeholder': 'Search Doctor'}),
        label="Doctor"
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            
        }

class PublicOnlineAppointmentForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date of Birth",
        required=True
    )

    class Meta:
        model = PublicOnlineAppointment
        fields = ['department', 'doctor', 'patient_full_name','birth_date', 'patient_phone', 'patient_email', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'patient_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date')
        appointment_date = cleaned_data.get('appointment_date')

        if birth_date and appointment_date:
            if birth_date >= appointment_date:
                raise forms.ValidationError("Date of Birth must be before the Appointment Date.")

        # Calculate age and validate it
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if age < 0 or age > 150:  # Ensure a valid age range
            raise forms.ValidationError("Invalid birth date. Please enter a valid date.")

        cleaned_data['age'] = age  # Store age for later use
        return cleaned_data