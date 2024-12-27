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