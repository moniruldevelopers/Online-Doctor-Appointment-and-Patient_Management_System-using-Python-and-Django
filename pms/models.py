from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid




# doctor profile 
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    full_name = models.CharField(max_length=100)  # Full name field
    specialization = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(
        max_length=11,        
        validators=[
            RegexValidator(
                regex=r'^01[3-9]\d{8}$',
                message="Enter a valid Bangladesh phone number (e.g., 01712345678).",
                code='invalid_phone'
            )
        ]
    ) 
    image = models.ImageField(upload_to='doctor_profile_image')  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} - {self.department.name if self.department else 'No Department'}"






# patient profile
class PatientIDTracker(models.Model):
    last_patient_id = models.BigIntegerField(default=1000000000)  # Start with 1000000000

    @staticmethod
    def generate_patient_id():
        """Generate a unique 10-digit sequential patient ID."""
        tracker, created = PatientIDTracker.objects.get_or_create(id=1)  # Ensure only one record
        new_patient_id = tracker.last_patient_id + 1
        tracker.last_patient_id = new_patient_id
        tracker.save()
        return str(new_patient_id)



class PatientProfile(models.Model):
    # Linking to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    
    # Unique patient ID
    patient_id = models.CharField(max_length=10, unique=True, editable=False)

    # Personal Information
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=gender_choices)
    phone_number = models.CharField(
        max_length=11,        
        validators=[
            RegexValidator(
                regex=r'^01[3-9]\d{8}$',
                message="Enter a valid Bangladesh phone number (e.g., 01712345678).",
                code='invalid_phone'
            )
        ]
    )

    # Address Information
    present_address = models.CharField(max_length=255, blank=True, null=True)
    permanent_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # Medical Information
    blood_type_choices = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                          ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]
    blood_type = models.CharField(max_length=3, choices=blood_type_choices, blank=True, null=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)

    # Health Conditions (Checkboxes for HIV, Thalassemia, etc.)
    allergies = models.BooleanField(default=False, blank=True, null=True)
    HIV_positive = models.BooleanField(default=False, blank=True, null=True)
    thalassemia = models.BooleanField(default=False, blank=True, null=True)
    diabetes = models.BooleanField(default=False, blank=True, null=True)
    hypertension = models.BooleanField(default=False, blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} (ID: {self.patient_id})"

    def save(self, *args, **kwargs):
        # Auto-generate patient ID if not already set
        if not self.patient_id:
            self.patient_id = PatientIDTracker.generate_patient_id()
        super().save(*args, **kwargs)





class SiteInfo(models.Model):
    site_name = models.CharField(max_length=20)
    color_logo = models.ImageField(upload_to='logo/')
    white_logo = models.ImageField(upload_to='logo/')
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=100)
    site_facebook = models.URLField(max_length=100)
    site_x = models.URLField(max_length=100)
    site_instagram = models.URLField(max_length=100)
    site_pinterest = models.URLField(max_length=100)

    def __str__(self):
        return self.site_name

    def clean(self):
        if SiteInfo.objects.exists() and not self.pk:
            raise ValidationError("Only one SiteInfo instance is allowed.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean method before saving
        super().save(*args, **kwargs)