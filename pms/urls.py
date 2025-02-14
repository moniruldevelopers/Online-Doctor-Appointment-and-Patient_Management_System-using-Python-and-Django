
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [   
    path('',home,name='home'),

    path('site-info/', site_info_view, name='site-info'),
    path("contact/", contact_view, name="contact"),
    path('contact-list/', contact_list_view, name='contact_list'),  # URL for the contact list page
    path('about/', about_us, name='about_us'),

    path('team-members/', team_member_list, name='team_member_list'),
    path('team-members/add/', add_team_member, name='add_team_member'),
    path('team-members/edit/<int:pk>/', edit_team_member, name='edit_team_member'),

    path('services/', service_list, name='service_list'),  # List services
    path('service/add/', service_view, name='add_service'),  # Add service
    path('service/edit/<int:pk>/', service_view, name='edit_service'),  # Edit service
    path('public-services/', public_service_list, name='public_service_list'),
  
    path('doctors/', public_doctor_list, name='public_doctor_list'),



    path('carousel/', carousel_list, name='carousel_list'),
    path('carousel/add/', add_carousel, name='add_carousel'),
    path('carousel/edit/<int:carousel_id>/', edit_carousel, name='edit_carousel'),
  

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
  
    #online appointmnet
    path("online-appointment/", public_online_appointment_view, name="public_online_appointment"),
    path("load-doctors/", load_doctors, name="load_doctors"),


    # public online appointment
    path('public-appointments/', public_online_appointment_list, name='public_online_appointment_list'),
    path('public-appointments/delete/<int:appointment_id>/', delete_public_online_appointment, name='delete_public_online_appointment'),
    path('public-appointments/export/', export_public_online_appointments_to_excel, name='export_public_online_appointments_to_excel'),
   
    # dashboard
    path('active-appointments/', active_appointments, name='active_appointments'),




]
