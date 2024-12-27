
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [   
    path('',home,name='home'),
    # patient section 

    path('patient_admin/', patient_admin, name='patient_admin'),
    path('view_profile/', view_profile, name='view_profile'),
    path('manage_profile/',manage_profile, name='manage_profile'),

    #hospital
    path('hospital_admin/', hospital_admin, name='hospital_admin'),
    path('manage-doctor-profile/', manage_doctor_profile, name='manage_doctors'),
    path('doctors/', view_all_doctors, name='view_all_doctors'),  
    path('doctor/update/<int:pk>/', update_doctor_profile, name='update_doctor_profile'),
    path('doctor/delete/<int:pk>/', delete_doctor_profile, name='delete_doctor_profile'),

    #role management
    path('roles/',manage_roles, name='manage_roles'),
    path('roles/create/', create_group, name='create_group'),
    path('roles/delete/<int:group_id>/', delete_group, name='delete_group'),
    # path('roles/update_permissions/<int:group_id>/', update_group_permissions, name='update_group_permissions'),
    path('update_permissions/<int:group_id>/', update_group_permissions, name='update_group_permissions'),
    path('roles/assign_group/', assign_group_to_user, name='assign_group_to_user'),
    path('get-username-suggestions/', get_username_suggestions, name='get_username_suggestions'),
    path('remove-group/', remove_group_from_user, name='remove_group_from_user'),
    path('staff-superusers/', show_staff_superusers, name='show_staff_superusers'),
 
]
