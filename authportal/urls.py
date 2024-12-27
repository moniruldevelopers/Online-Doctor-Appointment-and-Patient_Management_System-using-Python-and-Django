from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import handler404
# from blood.views import handler404 as custom_handler404
from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


# handler404 = custom_handler404


urlpatterns = [
   
    path('login/',loginuser, name='login'),
    path('logout/',logoutuser, name='logout'),
    # path('signup/',register, name='signup'),

    path('confirm_email/',confirm_email, name='confirm_email'),
    path('change_password/',change_password, name='change_password'),
    path('admin_change_password/',admin_change_password, name='admin_change_password'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),


    path('reset/password/',PasswordResetView.as_view(template_name='authportal/reset_password.html'), name='password_reset'),

    path('reset/password/done/',PasswordResetDoneView.as_view(template_name='authportal/reset_password_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='authportal/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done',PasswordResetCompleteView.as_view(template_name='authportal/password_reset_complete_done.html'), name='password_reset_complete'),


]
