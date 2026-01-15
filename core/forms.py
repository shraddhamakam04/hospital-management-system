from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DoctorProfile, PatientProfile, AvailabilitySlot
from django.utils import timezone
from django.core.exceptions import ValidationError

class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address'
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    specialization = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, numbers and @/./+/-/_ only.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize error messages
        self.fields['username'].error_messages = {
            'unique': 'This username is already taken. Please choose a different one.',
            'invalid': 'Username can only contain letters, numbers and @/./+/-/_ characters.',
            'required': 'Username is required.',
        }
        self.fields['email'].error_messages = {
            'unique': 'An account with this email already exists.',
            'invalid': 'Please enter a valid email address.',
            'required': 'Email is required.',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Try: ' + username + str(User.objects.count() + 1))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address'
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, numbers and @/./+/-/_ only.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize error messages
        self.fields['username'].error_messages = {
            'unique': 'This username is already taken. Please choose a different one.',
            'invalid': 'Username can only contain letters, numbers and @/./+/-/_ characters.',
            'required': 'Username is required.',
        }
        self.fields['email'].error_messages = {
            'unique': 'An account with this email already exists.',
            'invalid': 'Please enter a valid email address.',
            'required': 'Email is required.',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Try: ' + username + str(User.objects.count() + 1))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class AvailabilitySlotForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()})
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    
    class Meta:
        model = AvailabilitySlot
        fields = ['date', 'start_time', 'end_time']
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if date and date < timezone.now().date():
            raise forms.ValidationError("Cannot create slots in the past.")
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data