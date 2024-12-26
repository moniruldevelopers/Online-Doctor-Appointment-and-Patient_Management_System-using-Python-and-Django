
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


]
