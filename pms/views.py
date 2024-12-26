from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
# patient profile 
from django.shortcuts import render, redirect
from .models import PatientProfile
from .forms import PatientProfileForm
from django.contrib.auth.decorators import login_required

def view_profile(request):
    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
        return render(request, 'patient/patient_profile_view.html', {'profile': patient_profile})
    except PatientProfile.DoesNotExist:
        messages.info(request, "You don't have a profile. Please create one.")
        return redirect('manage_profile')

@login_required
def manage_profile(request):
    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        patient_profile = None

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('view_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientProfileForm(instance=patient_profile)

    return render(request, 'patient/manage_profile.html', {'form': form})


# Create your views here.
def home(request):
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance
    context = {
        'site_info': site_info,
    }
    return render (request, 'home.html', context)




def patient_admin(request):
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance
    context = {
        'site_info': site_info,
    }
    return render(request, 'patient/patient_home.html')

def hospital_admin(request):
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance
    context = {
        'site_info': site_info,
    }
    return render(request, 'hospital/hospital_home.html')



#doctor profile # Check function to allow only superusers or staff users
def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_superuser_or_staff, login_url='login')  # Redirect unauthorized users to login
def manage_doctor_profile(request, pk=None):
    if pk:
        doctor_profile = get_object_or_404(DoctorProfile, pk=pk)
    else:
        doctor_profile = None

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST,request.FILES, instance=doctor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile saved successfully!")
            return redirect('view_all_doctors')
        else:
            messages.error(request, "Error saving doctor profile. Please check the form.")
    else:
        form = DoctorProfileForm(instance=doctor_profile)

    context = {
        'form': form,
        'doctor_profile': doctor_profile,
    }
    return render(request, 'hospital/manage_doctor_profile.html', context)


def view_all_doctors(request):
    # Get all doctor profiles
    doctors = DoctorProfile.objects.all()

    # Render the list of doctors to the template
    context = {
        'doctors': doctors,
    }
    return render(request, 'hospital/view_all_doctors.html', context)


def update_doctor_profile(request, pk):
    doctor_profile = get_object_or_404(DoctorProfile, pk=pk)

    # Handle the form submission
    if request.method == 'POST':
        form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=doctor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile updated successfully!")
            return redirect('view_all_doctors')  # Redirect to the list of doctors
        else:
            messages.error(request, "Error updating doctor profile. Please check the form.")
    else:
        form = DoctorProfileUpdateForm(instance=doctor_profile)

    context = {
        'form': form,
        'doctor_profile': doctor_profile,
    }
    return render(request, 'hospital/updateprofile.html', context)

def delete_doctor_profile(request, pk):
    doctor_profile = get_object_or_404(DoctorProfile, pk=pk)
    
    if request.method == 'POST':
        doctor_profile.delete()
        messages.success(request, "Doctor profile deleted successfully!")
        return redirect('view_all_doctors')

    return redirect('view_all_doctors')  # If the request is not POST, simply redirect