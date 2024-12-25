from django.contrib import admin
from .models import *
# Register your models here.
from import_export import resources
from import_export.admin import ExportMixin


from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

class UserAdmin(DefaultUserAdmin):
    list_display = ( 'is_active','username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)






