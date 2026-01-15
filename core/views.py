from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .forms import DoctorSignUpForm, PatientSignUpForm, AvailabilitySlotForm
from .models import User, AvailabilitySlot, Booking
from .email_service import send_email


def home(request):
    return render(request, 'core/home.html')


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email('SIGNUP_WELCOME', user.email, {
                'name': user.get_full_name(),
                'role': 'Doctor'
            })
            login(request, user)
            messages.success(request, 'Welcome! Your doctor account has been created.')
            return redirect('dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'role': 'Doctor'})

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email('SIGNUP_WELCOME', user.email, {
                'name': user.get_full_name(),
                'role': 'Patient'
            })
            login(request, user)
            messages.success(request, 'Welcome! Your patient account has been created.')
            return redirect('dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'role': 'Patient'})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    if request.user.role == 'doctor':
        slots = AvailabilitySlot.objects.filter(doctor=request.user).order_by('date', 'start_time')
        bookings = Booking.objects.filter(availability_slot__doctor=request.user).select_related('patient', 'availability_slot')
        return render(request, 'core/doctor_dashboard.html', {
            'slots': slots,
            'bookings': bookings
        })
    else:
        doctors = User.objects.filter(role='doctor')
        bookings = Booking.objects.filter(patient=request.user).select_related('availability_slot__doctor')
        return render(request, 'core/patient_dashboard.html', {
            'doctors': doctors,
            'bookings': bookings
        })


@login_required
def create_availability(request):
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can create availability slots')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            messages.success(request, 'Availability slot created successfully')
            return redirect('dashboard')
    else:
        form = AvailabilitySlotForm()
    
    return render(request, 'core/create_availability.html', {'form': form})


@login_required
def view_available_slots(request, doctor_id):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments')
        return redirect('dashboard')
    
    doctor = get_object_or_404(User, id=doctor_id, role='doctor')
    available_slots = AvailabilitySlot.objects.filter(
        doctor=doctor,
        is_booked=False,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')
    
    return render(request, 'core/available_slots.html', {
        'doctor': doctor,
        'slots': available_slots
    })


@login_required
@transaction.atomic
def book_appointment(request, slot_id):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments')
        return redirect('dashboard')
    
    if request.method == 'POST':
        slot = get_object_or_404(
             AvailabilitySlot.objects.select_for_update(),
            id=slot_id,
            is_booked=False
        )
        
        if slot.date < timezone.now().date():
            messages.error(request, 'Cannot book past slots')
            return redirect('dashboard')
        
        # Create booking
        booking = Booking.objects.create(
            patient=request.user,
            availability_slot=slot
        )
        slot.is_booked = True
        slot.save()
        
        # Send confirmation emails
        send_email('BOOKING_CONFIRMATION', request.user.email, {
            'patient_name': request.user.get_full_name(),
            'doctor_name': slot.doctor.get_full_name(),
            'date': slot.date.strftime('%Y-%m-%d'),
            'time': slot.start_time.strftime('%H:%M')
        })
        
        send_email('BOOKING_CONFIRMATION', slot.doctor.email, {
            'patient_name': request.user.get_full_name(),
            'doctor_name': slot.doctor.get_full_name(),
            'date': slot.date.strftime('%Y-%m-%d'),
            'time': slot.start_time.strftime('%H:%M')
        })
        
        messages.success(request, 'Appointment booked successfully!')
        return redirect('dashboard')
    
    return redirect('dashboard')