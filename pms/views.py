from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages

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