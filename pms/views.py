from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
# patient profile 
from django.shortcuts import render, redirect
from .models import *
from .forms import PatientProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User,Permission
from django.db.models import Q
from django.http import JsonResponse
from .forms import GroupForm
from authportal.forms import *
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max
from datetime import datetime
from django.http import HttpResponseForbidden
from dateutil.relativedelta import relativedelta
import xlwt
import csv
from django.utils.dateparse import parse_date
from dateutil.relativedelta import relativedelta
import openpyxl
from django.utils.timezone import now


# Function to check if the user is a superuser
def superuser_required(user):
    return user.is_superuser





@login_required
@user_passes_test(superuser_required)
def site_info_view(request):
    site_info = SiteInfo.objects.first()  # Get the only existing instance

    if request.method == "POST":
        form = SiteInfoForm(request.POST, request.FILES, instance=site_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Site information updated successfully!")
            return redirect('site-info')  # Redirect to the same page after saving
    else:
        form = SiteInfoForm(instance=site_info)

    return render(request, 'site_info.html', {'form': form})



@login_required
@user_passes_test(superuser_required)
def contact_view(request):
    # Get the site information
    site_info = SiteInfo.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to prevent duplicate form submission
    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form,
        "site_info": site_info
    })

@login_required
@user_passes_test(superuser_required)
def contact_list_view(request):
    # Fetch all the contacts from the database
    contacts = Contact.objects.all().order_by('-sent_at')  # Order by sent_at (most recent first)
    
    # Paginate the contacts, showing 3 items per page
    paginator = Paginator(contacts, 3)
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the Page object for the current page
    
    return render(request, "contact_list.html", {"page_obj": page_obj})

def team_member_list(request):
    team_members = TeamMember.objects.all()
    if request.method == 'POST' and 'delete_team_member' in request.POST:
        team_member_id = request.POST.get('delete_team_member')
        team_member = get_object_or_404(TeamMember, pk=team_member_id)
        team_member.delete()
        messages.success(request, 'Team member deleted successfully!')
        return redirect('team_member_list')
    return render(request, 'team_member_list.html', {'team_members': team_members})

def add_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('team_member_list')
    else:
        form = TeamMemberForm()
    return render(request, 'add_team_member.html', {'form': form})

def edit_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('team_member_list')
    else:
        form = TeamMemberForm(instance=team_member)
    return render(request, 'add_team_member.html', {'form': form, 'edit_mode': True})

def about_us(request):
    team_members = TeamMember.objects.all()
    return render(request, 'about_us.html', {'team_members': team_members})



# View to list all services and handle delete operation
def service_list(request):
    services = Service.objects.all()
    
    if request.method == 'POST' and 'delete_service' in request.POST:
        service_id = request.POST.get('delete_service')
        service = get_object_or_404(Service, pk=service_id)
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('service_list')
    
    return render(request, 'service_list.html', {'services': services})

# View for adding and editing a service
def service_view(request, pk=None):
    if pk:
        service = get_object_or_404(Service, pk=pk)  # If editing, fetch the existing service
    else:
        service = None  # If adding, no service

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully!')
            return redirect('service_list')  # Redirect to service list after adding/editing
    else:
        form = ServiceForm(instance=service)  # Populate form with existing service or blank form

    return render(request, 'service_form.html', {'form': form, 'service': service})

def public_service_list(request):
    services = Service.objects.all()
    return render(request, 'public_service_list.html', {'services': services})

def public_doctor_list(request):
    # Fetch active doctors
    doctors = DoctorProfile.objects.filter(is_active=True)
    return render(request, 'public_doctor_list.html', {'doctors': doctors})





def carousel_list(request):
    carousels = Carousel.objects.all()

    if request.method == 'POST' and 'delete_carousel' in request.POST:
        carousel_id = request.POST.get('delete_carousel')
        carousel = get_object_or_404(Carousel, pk=carousel_id)
        carousel.delete()
        messages.success(request, "Carousel slide deleted successfully!")
        return redirect('carousel_list')

    return render(request, 'carousel_list.html', {'carousels': carousels})







# Add a new carousel slide
def add_carousel(request):
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Carousel slide added successfully!")
            return redirect('carousel_list')
    else:
        form = CarouselForm()
    
    return render(request, 'carousel_form.html', {'form': form})

# Edit an existing carousel slide
def edit_carousel(request, carousel_id):
    carousel = get_object_or_404(Carousel, id=carousel_id)
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES, instance=carousel)
        if form.is_valid():
            form.save()
            messages.success(request, "Carousel slide updated successfully!")
            return redirect('carousel_list')
    else:
        form = CarouselForm(instance=carousel)

    return render(request, 'carousel_form.html', {'form': form})


















def success_page(request):
    return render(request, 'success.html')



def home(request):
    site_info = SiteInfo.objects.first()  # Fetch site info data
    doctors = DoctorProfile.objects.all().order_by('-id')[:2]  # Get last 2 added doctors
    carousels = Carousel.objects.all().order_by('-id')[:3]  # Get last 3 added carousel items


    departments = Department.objects.all()
    
    context = {
        'site_info': site_info,       
        'doctors': doctors,  # Pass only the last two doctors
        'carousels': carousels,  # Pass last 3 carousel items
    }
    return render(request, 'home.html', context)

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




















def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirect to the appointment list or another page
    else:
        form = AppointmentForm()
    return render(request, 'hospital/create_appointment.html', {'form': form})

# AJAX to auto-populate department and patient phone
def get_doctor_details(request):
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        return JsonResponse({'department': doctor.department.name if doctor.department else 'No Department'})
    return JsonResponse({'department': 'No Department'})

def get_patient_details(request):
    patient_id = request.GET.get('patient_id')
    if patient_id:
        patient = get_object_or_404(PatientProfile, id=patient_id)
        return JsonResponse({'phone_number': patient.phone_number})
    return JsonResponse({'phone_number': ''})





def export_to_excel(appointments, department_name, doctor_name, selected_date):
    """
    Export filtered appointments to a CSV file.
    """
    file_date = selected_date if selected_date else "all_dates"
    # Update file name to include doctor and department names
    file_name = f"{doctor_name}_{department_name}_appointments_{file_date}.csv".replace(" ", "_")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    writer = csv.writer(response)
    writer.writerow(['Serial Number', 'Patient ID', 'Patient Phone', 'Patient Age', 'Doctor Name', 'Department', 'Date'])

    for appointment in appointments:
        writer.writerow([ 
            appointment.serial_number,
            appointment.patient_unique_id,
            appointment.patient.phone_number,
            getattr(appointment, 'patient_age', 'N/A'),
            appointment.doctor.full_name,
            appointment.doctor.department.name,
            appointment.appointment_date.strftime('%Y-%m-%d'),
        ])

    return response






def appointment_list(request):
    doctor_filter = request.GET.get('doctor')
    selected_date = request.GET.get('date')

    # Ensure selected_date is always a valid string before parsing
    if selected_date:
        selected_date = parse_date(selected_date)  # Convert string to date object
    else:
        selected_date = datetime.today().date()  # Default to today's date

    appointments = Appointment.objects.select_related('patient', 'doctor', 'doctor__department')

    if doctor_filter:
        appointments = appointments.filter(doctor__id=doctor_filter)

    # Filter appointments by the selected date (default to today)
    appointments = appointments.filter(appointment_date__date=selected_date)

    # Calculate patient age
    today = datetime.today().date()
    for appointment in appointments:
        if appointment.patient.date_of_birth:
            dob = appointment.patient.date_of_birth
            age = relativedelta(today, dob)
            age_parts = []
            if age.years > 0:
                age_parts.append(f"{age.years} year{'s' if age.years > 1 else ''}")
            if age.months > 0:
                age_parts.append(f"{age.months} month{'s' if age.months > 1 else ''}")
            if age.days > 0:
                age_parts.append(f"{age.days} day{'s' if age.days > 1 else ''}")
            appointment.patient_age = ", ".join(age_parts) if age_parts else "0 days"
        else:
            appointment.patient_age = "Age not available"

    # Handle export
    if 'export' in request.GET:
        doctor = DoctorProfile.objects.filter(id=doctor_filter).first() if doctor_filter else None
        doctor_name = doctor.full_name if doctor else "All_Doctors"
        department_name = doctor.department.name if doctor else "All_Departments"
        return export_to_excel(appointments, department_name, doctor_name, selected_date)

    doctors = DoctorProfile.objects.all()

    # Show a message indicating which doctor is selected for which date
    filtered_doctor_name = "All Doctors"
    if doctor_filter:
        doctor = DoctorProfile.objects.filter(id=doctor_filter).first()
        if doctor:
            filtered_doctor_name = doctor.full_name

    filter_message = f"Showing appointments for {filtered_doctor_name} on {selected_date.strftime('%Y-%m-%d')}."

    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments,
        'doctors': doctors,
        'doctor_filter': doctor_filter,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'filter_message': filter_message,  # Send filter message to the template
    })





def public_online_appointment_view(request):
    form = PublicOnlineAppointmentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment booked successfully!")
            form = PublicOnlineAppointmentForm()  # Reset the form after submission

    return render(request, "public_online_appointment_form.html", {"form": form})


def load_doctors(request):
    department_id = request.GET.get('department')
    doctors = DoctorProfile.objects.filter(department_id=department_id, is_active=True).values('id', 'full_name')
    return JsonResponse(list(doctors), safe=False)











def public_online_appointment_list(request):
    # Get filter parameters
    doctor = request.GET.get('doctor')
    appointment_date = request.GET.get('date')

    # Validate and parse the date
    if appointment_date:
        appointment_date = parse_date(appointment_date)
        if not appointment_date:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            appointment_date = date.today()
    else:
        appointment_date = date.today()

    # Filter appointments
    appointments = PublicOnlineAppointment.objects.filter(appointment_date=appointment_date)
    if doctor:
        appointments = appointments.filter(doctor_id=doctor)

    # Get distinct doctors for the filter
    doctors = PublicOnlineAppointment.objects.values_list('doctor__id', 'doctor__full_name').distinct()

    return render(request, 'patient/public_online_appointment_list.html', {
        'appointments': appointments,
        'doctors': doctors,
        'appointment_date': appointment_date,
        'selected_doctor': doctor,
    })


def delete_public_online_appointment(request, appointment_id):
    appointment = PublicOnlineAppointment.objects.filter(appointment_id=appointment_id).first()
    if appointment:
        appointment.delete()
        messages.success(request, "Appointment deleted successfully!")
    else:
        messages.error(request, "Appointment not found!")
    return redirect('public_online_appointment_list')

# Export appointments to an Excel (XLSX) file
def export_public_online_appointments_to_excel(request):
    doctor_id = request.GET.get('doctor')
    appointment_date_str = request.GET.get('date')  # Get date as string

    # Convert date string to date object
    if appointment_date_str:
        try:
            appointment_date = date.fromisoformat(appointment_date_str)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect('public_online_appointment_list')
    else:
        appointment_date = None

    # Start with all appointments
    appointments = PublicOnlineAppointment.objects.all()

    # Apply filters
    doctor_name = "All_Doctors"
    department_name = "All_Departments"

    if doctor_id:
        try:
            doctor_id = int(doctor_id)
            appointments = appointments.filter(doctor_id=doctor_id)
            doctor = PublicOnlineAppointment.objects.filter(doctor_id=doctor_id).first()
            if doctor:
                doctor_name = doctor.doctor.full_name
                department_name = doctor.department.name
        except ValueError:
            pass

    if appointment_date:
        appointments = appointments.filter(appointment_date=appointment_date)

    # Create Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Appointments"

    # Header row
    headers = ['ID', 'Department', 'Doctor', 'Patient Name', 'Phone', 'Email', 'Date']
    ws.append(headers)

    # Data rows
    for appointment in appointments:
        ws.append([
            appointment.appointment_id,
            appointment.department.name,  
            appointment.doctor.full_name, 
            appointment.patient_full_name,
            appointment.patient_phone,
            appointment.patient_email,
            appointment.appointment_date,
        ])

    # Generate file name
    filename = f"{doctor_name}_{department_name}.xlsx".replace(" ", "_")

    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Save workbook to response
    wb.save(response)
    return response





def active_appointments(request):
    doctor_id = request.GET.get('doctor')
    appointment_date = request.GET.get('date')

    # Get today's date
    today = now().date()

    # Start with all future appointments
    appointments = Appointment.objects.filter(appointment_date__date__gte=today)
    online_appointments = PublicOnlineAppointment.objects.filter(appointment_date__gte=today)

    # Apply doctor filter
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
        online_appointments = online_appointments.filter(doctor_id=doctor_id)

    # Apply date filter
    if appointment_date:
        appointments = appointments.filter(appointment_date__date=appointment_date)
        online_appointments = online_appointments.filter(appointment_date=appointment_date)

    # Combine results
    all_appointments = list(appointments) + list(online_appointments)

    # Get a list of doctors for filtering
    doctors = set([(appt.doctor.id, appt.doctor.full_name) for appt in Appointment.objects.all()] +
                  [(appt.doctor.id, appt.doctor.full_name) for appt in PublicOnlineAppointment.objects.all()])

    return render(request, 'hospital/active_appointments.html', {
        'appointments': all_appointments,
        'doctors': sorted(doctors, key=lambda x: x[1]),  # Sort by doctor name
        'selected_doctor': doctor_id,
        'appointment_date': appointment_date,
    })