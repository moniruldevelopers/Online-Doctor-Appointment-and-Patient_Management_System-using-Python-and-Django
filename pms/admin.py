from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.html import format_html

from .models import *

# Register your models here.
from django.utils.html import mark_safe

#my customizations
admin.site.site_header = "Patient Management ADMIN PANEL"
admin.site.site_title = "Patient Management ADMIN PANEL"
admin.site.index_title = "Welcome to Patient Management PORTAL"


class SiteInfoAdminForm(ModelForm):
    class Meta:
        model = SiteInfo
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        if SiteInfo.objects.exists() and not self.instance.pk:
            raise ValidationError("Only one SiteInfo instance is allowed.")
        return cleaned_data

class SiteInfoAdmin(admin.ModelAdmin):
    form = SiteInfoAdminForm

admin.site.register(SiteInfo, SiteInfoAdmin)




# patient profile
admin.site.register(PatientProfile)
admin.site.register(Department)
admin.site.register(DoctorProfile)
admin.site.register(EmployeeProfile)
admin.site.register(Appointment)
admin.site.register(PublicOnlineAppointment)
