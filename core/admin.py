from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorProfile, PatientProfile, AvailabilitySlot, Booking

admin.site.register(User, UserAdmin)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(AvailabilitySlot)
admin.site.register(Booking)