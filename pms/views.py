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
from django.db.models import Max
from datetime import datetime
from django.http import HttpResponseForbidden


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

            # Redirect to the doctor profile update page for the new user
            messages.success(request, 'Account created successfully! Please complete the doctor profile.')
            return redirect('user_to_doctor_profile', user_id=user.id)
    else:
        form = CustomSignUpForm()

    return render(request, 'hospital/auth/employee_signup.html', {'form': form})


#user to doctorprofile update function
def user_to_doctor_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the user already has a DoctorProfile
    try:
        doctor_profile = DoctorProfile.objects.get(user=user)
    except DoctorProfile.DoesNotExist:
        doctor_profile = None

    if request.method == "POST":
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor_profile)
        if form.is_valid():
            # Only create or update the DoctorProfile when the form is valid
            if not doctor_profile:  # Create new profile if none exists
                doctor_profile = form.save(commit=False)
                doctor_profile.user = user
                doctor_profile.save()
            else:
                form.save()  # Update the existing profile

            messages.success(request, 'Doctor profile updated successfully!')
            return redirect('all_doctors')  # Redirect to the doctors list or any desired page
    else:
        form = DoctorProfileForm(instance=doctor_profile)

    return render(request, 'hospital/doctor_profile/user_to_doctor_update_profile.html', {'form': form, 'user': user})


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
def generate_sequential_username():
    # Get the current year
    current_year = datetime.now().year

    # Find the highest existing username for the current year
    prefix = f"{current_year}"
    max_username = User.objects.filter(username__startswith=prefix).aggregate(
        max_username=Max('username')
    )['max_username']

    if max_username:
        # Extract the numeric part and increment it
        last_number = int(max_username[len(prefix):])  # Remove the prefix to get the number
        new_number = last_number + 1
    else:
        # Start from 1 if no usernames exist for the current year
        new_number = 1

    # Format the new username
    sequential_username = f"{prefix}{new_number:06d}"  # Pad to 6 digits
    return sequential_username

def get_generated_username(request):
    if request.method == "GET":
        username = generate_sequential_username()
        return JsonResponse({'username': username})




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

            # Generate a sequential username
            username = generate_sequential_username()

            # Save the user and activate
            user = form.save(commit=False)
            user.username = username  # Set the generated username
            user.is_active = True
            user.save()

            # Redirect to the patient profile update page
            messages.success(request, f'Account created successfully! Your username is {username}. Please complete the patient profile.')
            return redirect('user_to_patient_profile', user_id=user.id)
    else:
        form = CustomSignUpForm()

    return render(request, 'hospital/auth/signup.html', {'form': form})


#user to doctorprofile update functiondef user_to_patient_profile(request, user_id):
def user_to_patient_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the user already has a PatientProfile
    try:
        patient_profile = PatientProfile.objects.get(user=user)
    except PatientProfile.DoesNotExist:
        patient_profile = None

    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            # Only create or update the PatientProfile when the form is valid
            if not patient_profile:  # Create new profile if none exists
                patient_profile = form.save(commit=False)
                patient_profile.user = user
                patient_profile.save()
            else:
                form.save()  # Update the existing profile

            messages.success(request, 'Patient profile updated successfully!')
            return redirect('all_patients')  # Redirect to your desired page
    else:
        form = PatientProfileForm(instance=patient_profile)

    return render(request, 'patient/user_to_patient_update_profile.html', {'form': form, 'user': user})



def all_patients(request):
    search_query = request.GET.get('search', '')  # Get search query from URL
    patients = PatientProfile.objects.all().order_by('-id')

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
    username = patient.user.username if patient.user else 'N/A'
    password = username  # Password is set to be the same as the username
    email = patient.user.email if patient.user else 'N/A'

    context = {
        'patient': patient,
        'site_info': site_info,
        'username': username,
        'password': password,
        'email': email,
    }
    return render(request, 'patient/view_patient_profile.html', context)




#employee profile create def admin_employee_register(request):

def admin_employee_register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            # Check if the email domain is valid and if it ends with '@gmail.com'
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('admin_employee_register')

            if not email.endswith('@gmail.com'):
                messages.error(request, 'Please use a valid @gmail.com email address.')
                return redirect('admin_employee_register')

            user = form.save(commit=False)
            user.is_active = True  # Automatically activate the user
            user.save()

            # Redirect to manage employee profile for the new user
            messages.success(request, 'Account created successfully! Please complete the employee profile.')
            return redirect('user_to_employee_profile', user_id=user.id)
    else:
        form = CustomSignUpForm()

    return render(request, 'hospital/auth/employee_signup.html', {'form': form})


def user_to_employee_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the user already has an EmployeeProfile
    try:
        employee_profile = EmployeeProfile.objects.get(user=user)
    except EmployeeProfile.DoesNotExist:
        employee_profile = None

    if request.method == "POST":
        # Only create the profile if it doesn't exist and the form is valid
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee_profile)
        if form.is_valid():
            # Save the profile only after it is filled out correctly
            if not employee_profile:  # Only create a new profile if it doesn't exist
                employee_profile = form.save(commit=False)
                employee_profile.user = user
                employee_profile.save()
            else:
                form.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('all_employee')
    else:
        form = EmployeeProfileForm(instance=employee_profile)

    return render(request, 'hospital/employee_profile/user_to_employee_update_profile.html', {'form': form})


def all_employee(request):    
    employees = EmployeeProfile.objects.filter(user__isnull=False).exclude(name__isnull=True).exclude(name__exact='')
    return render(request, 'hospital/employee_profile/all_employee.html', {'employees': employees})


def edit_employee(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('all_employee')
    else:
        form = EmployeeProfileForm(instance=employee)
    return render(request, 'hospital/employee_profile/edit_employee.html', {'form': form})


def delete_employee(request, pk):
    # Fetch the employee profile by primary key
    employee = get_object_or_404(EmployeeProfile, pk=pk)

    if request.method == "POST":
        # Deleting associated user along with the employee profile
        employee.user.delete()  # Deletes the associated user
        employee.delete()  # Deletes the employee profile

        # Add success message and redirect
        messages.success(request, 'Employee profile deleted successfully!')
        return redirect('all_employee')  # Redirect to the list of all employees

    # If method is GET, redirect directly (no confirmation page)
    return redirect('all_employee')  # Optionally, you can choose another redirect


# View to show all users excluding superusers, staff, and users with any group
# View to show all users excluding superusers, staff, and users with roles assigned
def all_users(request):
    # Get the search query if it exists
    search_query = request.GET.get('search', '')
    
    # Filter users excluding superusers, staff, and users with any group assigned
    users = User.objects.filter(is_superuser=False, is_staff=False, groups__isnull=True)
    
    if search_query:
        users = users.filter(username__icontains=search_query) | users.filter(email__icontains=search_query)
    
    # Order users by the 'date_joined' field in descending order to show the most recently added users first
    users = users.order_by('-date_joined')

    # Paginate the user list
    paginator = Paginator(users, 2)  # Show 2 users per page (adjust as needed)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'authportal/all_users.html', {
        'page_obj': page_obj, 
        'search_query': search_query
    })

# View to delete a user
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Ensure that the user cannot delete themselves
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('all_users')
    
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('all_users')
    
    # If the request method is not POST, return a forbidden response
    return HttpResponseForbidden("Invalid request method")