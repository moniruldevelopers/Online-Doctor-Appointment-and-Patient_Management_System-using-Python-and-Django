
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


]
