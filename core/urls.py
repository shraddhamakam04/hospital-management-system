from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('availability/create/', views.create_availability, name='create_availability'),
    path('doctor/<int:doctor_id>/slots/', views.view_available_slots, name='view_available_slots'),
    path('book/<int:slot_id>/', views.book_appointment, name='book_appointment'),
]