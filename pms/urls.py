
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [   
    path('',home,name='home'),
    # patient section 
    path("admin_patient_register/", admin_patient_register, name="admin_patient_register"),
    path('patient/<int:user_id>/update-profile/', user_to_patient_profile, name='user_to_patient_profile'),
    path('all_patients/', all_patients, name='all_patients'),
    path('patients/<int:patient_id>/view/', view_patient_profile, name='view_patient_profile'),
   
    path('patients/<int:patient_id>/update/', update_patient_profile, name='update_patient_profile'),
    path('patients/<int:pk>/delete/', delete_patient, name='delete_patient'),
    path('patient_admin/', patient_admin, name='patient_admin'),
    path('view_profile/', view_profile, name='view_profile'),

    #hospital
    path('hospital_admin/', hospital_admin, name='hospital_admin'),
    path('get-generated-username/', get_generated_username, name='get_generated_username'),

    # doctor
    path('admin_doctor_register/',admin_doctor_register, name='admin_doctor_register'),
    path('doctor/<int:user_id>/update-profile/', user_to_doctor_profile, name='user_to_doctor_profile'),
    path('doctors/all/', all_doctors, name='all_doctors'),  # Add this path
    path('doctors/<int:doctor_id>/', update_signle_doctor, name='update_doctor'),
    path('doctors/<int:doctor_id>/delete/', delete_doctor, name='delete_doctor'),

    #employee 
    path('admin_employee_register/',admin_employee_register, name='admin_employee_register'),
    path('user/<int:user_id>/employee-profile/', user_to_employee_profile, name='user_to_employee_profile'),
    path('employees/', all_employee, name='all_employee'),
    path('employees/edit/<int:pk>/', edit_employee, name='edit_employee'),  
    path('employees/delete/<int:pk>/', delete_employee, name='delete_employee'),

    


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


    # all user
    path('users/', all_users, name='all_users'),
    path('users/delete/<int:pk>/', delete_user, name='delete_user'),

    #create appointment
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('ajax/doctor-details/', get_doctor_details, name='get_doctor_details'),
    path('ajax/patient-details/', get_patient_details, name='get_patient_details'),
 
 
]
