from django.contrib import admin

# Register your models here.
from .models import User, PatientProfile, DoctorProfile

admin.site.register(User)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)