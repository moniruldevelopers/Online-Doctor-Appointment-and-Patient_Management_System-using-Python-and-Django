from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseBadRequest
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
from django.contrib.auth.models import Group, User,Permission
from django.db.models import Q
from django.http import JsonResponse
from .forms import GroupForm
from authportal.forms import *
from datetime import date
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


# website view section
def home(request):
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance
    context = {
        'site_info': site_info,
    }
    return render (request, 'home.html', context)





#patient section for patient
def view_profile(request):
    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
        return render(request, 'patient/patient_profile_view.html', {'profile': patient_profile})
    except PatientProfile.DoesNotExist:
        messages.info(request, "You don't have a profile. Please create one.")
        return redirect('all_patients')




def patient_admin(request):
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance
    context = {
        'site_info': site_info,
    }
    return render(request, 'patient/patient_home.html')





#hospital section
def hospital_admin(request):
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance
    context = {
        'site_info': site_info,
    }
    return render(request, 'hospital/hospital_home.html')







#role management
# Check if user is a superuser
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='login')
def manage_roles(request):
    groups = Group.objects.all()  # Get all groups (roles)
    return render(request, 'hospital/role_management/manage_roles.html', {'groups': groups})

@user_passes_test(is_superuser, login_url='login')
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group = Group.objects.create(name=group_name)  # Create a new group
        messages.success(request, f"Group '{group_name}' created successfully!")
        return redirect('manage_roles')
    
    return render(request, 'hospital/role_management/create_group.html')

@user_passes_test(is_superuser, login_url='login')
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()  # Delete the group
    messages.success(request, f"Group '{group.name}' deleted successfully!")
    return redirect('manage_roles')


def update_group_permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        # Extract permissions selected during form submission
        selected_permission_ids = set(map(int, request.POST.getlist('permissions_selected')))

        # Retain only explicitly selected permissions
        group.permissions.set(selected_permission_ids)

        messages.success(request, "Permissions updated successfully!")
        return redirect('manage_roles')

    # Permissions currently assigned to the group
    selected_permissions = group.permissions.all()
    # Permissions not yet assigned to the group
    available_permissions = Permission.objects.exclude(id__in=selected_permissions)

    return render(request, 'hospital/role_management/update_group_permissions.html', {
        'group': group,
        'available_permissions': available_permissions,
        'selected_permissions': selected_permissions,
    })


def get_username_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = User.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query)
    ).values_list('username', 'email')[:10]  # Limiting to 10 results
    suggestion_list = [f"{user[0]} ({user[1]})" for user in suggestions]  # Format as "username (email)"
    return JsonResponse({'suggestions': suggestion_list})

# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='login')
def assign_group_to_user(request):
    groups = Group.objects.all()  # Get all groups (roles)

    if request.method == 'POST':
        username = request.POST.get('username')
        group_id = request.POST.get('group_id')
        user = get_object_or_404(User, username=username)
        group = get_object_or_404(Group, id=group_id)

        # Assign the group to the user
        if group not in user.groups.all():
            user.groups.add(group)
            messages.success(request, f"Group '{group.name}' assigned to user '{user.username}' successfully!")
        else:
            messages.info(request, f"User '{user.username}' is already in group '{group.name}'.")

        # Update staff and superuser status
        user.is_staff = 'staff' in request.POST
        user.is_superuser = 'superuser' in request.POST
        user.save()  # Save updates

        # Redirect to the staff and superuser list
        return redirect('show_staff_superusers')

    return render(request, 'hospital/role_management/assign_group_to_user.html', {'groups': groups})



@user_passes_test(is_superuser, login_url='login')
def remove_group_from_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        group_id = request.POST.get('group_id')
        user = get_object_or_404(User, username=username)
        group = get_object_or_404(Group, id=group_id)

        # Remove group from user
        if group in user.groups.all():
            user.groups.remove(group)
            messages.success(request, f"Group '{group.name}' removed from user '{user.username}' successfully!")
        else:
            messages.error(request, f"Group '{group.name}' is not assigned to user '{user.username}'.")

        # Update staff and superuser status based on groups
        if not user.groups.exists():
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.info(request, f"User '{user.username}' is no longer a staff or superuser since they have no assigned groups.")
        
        return redirect('show_staff_superusers')

    return HttpResponseBadRequest("Invalid request.")



def show_staff_superusers(request):
    # Filter staff and superuser users
    staff_and_superusers = User.objects.filter(
        Q(is_staff=True) | Q(is_superuser=True)
    ).order_by('username')
    
    return render(request, 'hospital/role_management/show_staff_superusers.html', {
        'staff_and_superusers': staff_and_superusers
    })



#doctor section =================================================================================

def admin_doctor_register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            # Check if the email domain is valid and if it ends with '@gmail.com'
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('admin_doctor_register')  # Change from 'signup'

            if not email.endswith('@gmail.com'):
                messages.error(request, 'Please use a valid @gmail.com email address.')
                return redirect('admin_doctor_register')  # Change from 'signup'

            user = form.save(commit=False)
            user.is_active = True  # Automatically activate the user
            user.save()

            # Create a DoctorProfile instance for the new user
            DoctorProfile.objects.create(user=user)

            # Redirect to manage doctor profile for the new user
            messages.success(request, 'Account created successfully! Please complete the doctor profile.')
            return redirect('user_to_doctor_profile', user_id=user.id)
    else:
        form = CustomSignUpForm()

    return render(request, 'hospital/auth/signup.html', {'form': form})


#user to doctorprofile update function
def user_to_doctor_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    doctor_profile = get_object_or_404(DoctorProfile, user=user)

    if request.method == "POST":
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('all_doctors')  # Adjust this to redirect to the doctor's dashboard or profile view
    else:
        form = DoctorProfileForm(instance=doctor_profile)

    return render(request, 'hospital/doctor_profile/user_to_doctor_update_profile.html', {'form': form})



def all_doctors(request):
    # Only include doctors with a user and a non-empty full_name
    doctors = DoctorProfile.objects.filter(user__isnull=False).exclude(full_name__isnull=True).exclude(full_name__exact='')
    return render(request, 'hospital/doctor_profile/all_doctors.html', {'doctors': doctors})


def update_signle_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)  # Fetch doctor by ID
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile updated successfully!")
            return redirect('all_doctors')  # Redirect to the all doctors page
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, 'hospital/doctor_profile/update_single_doctor.html', {'form': form, 'doctor': doctor})
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    if request.method == 'POST':
        doctor.delete()
        return redirect('all_doctors')  # Replace with your "all doctors" URL name





#patient section =================================================================================

def admin_patient_register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            # Check if the email domain is valid and if it ends with '@gmail.com'
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('admin_patient_register')

            if not email.endswith('@gmail.com'):
                messages.error(request, 'Please use a valid @gmail.com email address.')
                return redirect('admin_patient_register')

            # Save the user and activate
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            # Redirect to the patient profile update page
            messages.success(request, 'Account created successfully! Please complete the patient profile.')
            return redirect('user_to_patient_profile', user_id=user.id)
    else:
        form = CustomSignUpForm()

    return render(request, 'hospital/auth/signup.html', {'form': form})

#user to doctorprofile update function
def user_to_patient_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Access the PatientProfile via the related_name
    patient_profile = getattr(user, 'patient_profile', None)

    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            # Ensure the user is linked to the profile
            form.instance.user = user
            form.save()
            messages.success(request, 'Patient profile updated successfully!')
            return redirect('all_patients')  # Replace with your desired redirect URL
    else:
        form = PatientProfileForm(instance=patient_profile)

    return render(request, 'patient/user_to_patient_update_profile.html', {'form': form, 'user': user})

def all_patients(request):
    search_query = request.GET.get('search', '')  # Get search query from URL
    patients = PatientProfile.objects.all()

    # Apply filtering based on search query (search by Patient ID or Phone Number)
    if search_query:
        patients = patients.filter(
            patient_id__icontains=search_query
        ) | patients.filter(
            phone_number__icontains=search_query
        )

    # Calculate age for each patient
    for patient in patients:
        if patient.date_of_birth:
            today = date.today()
            delta_years = today.year - patient.date_of_birth.year
            delta_months = today.month - patient.date_of_birth.month
            delta_days = today.day - patient.date_of_birth.day

            # If the patient is less than 1 year old
            if delta_years == 0:
                if delta_months == 0:  # Less than a month old
                    patient.age = f"{delta_days} day(s)"
                else:  # Less than a year old
                    patient.age = f"{delta_months} month(s)"
            else:
                # More than a year old
                if delta_months < 0:
                    delta_years -= 1
                    delta_months += 12
                if delta_days < 0:
                    delta_months -= 1
                    delta_days += 30  # Approximation

                patient.age = f"{delta_years} year(s), {delta_months} month(s), {delta_days} day(s)"
        else:
            patient.age = "N/A"

    # Pagination
    paginator = Paginator(patients, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'patient/all_patients.html', {'page_obj': page_obj, 'search_query': search_query})









def update_patient_profile(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('all_patients')  # Redirect to the list of patients after successful update
    else:
        form = PatientProfileForm(instance=patient)

    return render(request, 'patient/update_single_patient.html', {'form': form, 'patient': patient})





def delete_patient(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)
    if request.method == "POST":
        patient.user.delete()  # Deletes the associated user as well
        patient.delete()
        messages.success(request, 'Patient profile deleted successfully!')
        return redirect('all_patients')
    

def view_patient_profile(request, patient_id):
    # Retrieve the patient profile using the patient_id
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)
    
    # Calculate age for the patient
    if patient.date_of_birth:
        today = date.today()
        delta_years = today.year - patient.date_of_birth.year
        delta_months = today.month - patient.date_of_birth.month
        delta_days = today.day - patient.date_of_birth.day

        # If the patient is less than 1 year old
        if delta_years == 0:
            if delta_months == 0:  # Less than a month old
                patient.age = f"{delta_days} day(s)"
            else:  # Less than a year old
                patient.age = f"{delta_months} month(s)"
        else:
            # More than a year old
            if delta_months < 0:
                delta_years -= 1
                delta_months += 12
            if delta_days < 0:
                delta_months -= 1
                delta_days += 30  # Approximation for days

            patient.age = f"{delta_years} year(s), {delta_months} month(s), {delta_days} day(s)"
    else:
        patient.age = "N/A"

    # Fetch the site info for hospital branding
    site_info = SiteInfo.objects.first()  # Get the first (and only) instance of SiteInfo
    
    context = {
        'patient': patient,
        'site_info': site_info,
    }

    return render(request, 'patient/view_patient_profile.html', context)