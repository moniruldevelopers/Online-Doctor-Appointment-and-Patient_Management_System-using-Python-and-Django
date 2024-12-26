from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required

# for authentication
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.core.exceptions import ValidationError

#send mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel=get_user_model()




# for register last

from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import BadHeaderError
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
# pagination
from django.core.paginator import Paginator
from django.http import JsonResponse


def logoutuser(request):
    logout(request)
    messages.success(request, 'Logout Success')
    return redirect('login')


User = get_user_model()

def register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            # Check if the email domain is valid and if it ends with '@gmail.com'
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('signup')

            if not email.endswith('@gmail.com'):
                messages.error(request, 'Please use a valid @gmail.com email address.')
                return redirect('signup')
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()  # Save the user first, before sending the email
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('authportal/account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            email_message = EmailMessage(mail_subject, message, to=[email])
            email_message.send()

            messages.success(request, 'Account created successfully! Activate your account from the mail you provided.')
            return redirect('confirm_email')
    else:
        form = CustomSignUpForm()

    return render(request, 'authportal/signup.html', {'form': form})



def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, "Your account is activated now, you can now login")
        return redirect('login')
    else:
        messages.warning(request,"activation link is invalid")
        return redirect('signup')




def loginuser(request):
    # If the user is already logged in, check their role and redirect accordingly
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('/hospital_admin/')  # Redirect to the admin panel
        else:
            return redirect('patient_admin')  # Redirect to patient_admin if not superuser or staff

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if user.is_active:
                # Authenticate user
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)

                    # Check if user is superuser or staff and redirect accordingly
                    if user.is_superuser or user.is_staff:
                        return redirect('/hospital_admin/')  # Redirect to admin panel
                    else:
                        messages.success(request, 'Login Success')
                        return redirect('patient_admin')  # Redirect to patient admin

                else:
                    messages.error(request, 'Invalid Email or Password')
            else:
                # Send activation email if account is inactive
                current_site = get_current_site(request)
                mail_subject = 'Activate Your Account'
                message = render_to_string('authportal/account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

                email_message = EmailMessage(mail_subject, message, to=[email])
                email_message.send()

                messages.error(request, 'Your account is not activated. A new activation email has been sent.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Email or Password')

    # Handle GET request (show login form)
    return render(request, 'authportal/login.html', {'form': AuthenticationForm()})









def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Change Success')
            return redirect('login')  
    else:
        form = PasswordChangeForm(user=request.user) 
    return render(request, 'authportal/change_password.html', {'form':form}) 


def confirm_email(request):
    return render(request,'authportal/confirm_email_sent.html')








