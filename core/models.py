from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    google_calendar_credentials = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('doctor', 'date', 'start_time')
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.date} {self.start_time}-{self.end_time}"
    
    @property
    def is_available(self):
        return not self.is_booked and timezone.now().date() <= self.date


class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    availability_slot = models.OneToOneField(AvailabilitySlot, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    doctor_calendar_event_id = models.CharField(max_length=255, blank=True)
    patient_calendar_event_id = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.patient.get_full_name()} with {self.availability_slot.doctor.get_full_name()}"