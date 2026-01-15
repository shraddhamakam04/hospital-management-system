# Hospital Management System

A Django-based hospital management web application with doctor availability management, patient appointment booking, and serverless email notifications.

## 🚀 Features

### Core Functionality
- **User Authentication**: Separate registration and login for doctors and patients
- **Role-Based Access**: Different dashboards for doctors and patients
- **Doctor Features**:
  - Create and manage availability time slots
  - View all appointments
  - See booking status of time slots
- **Patient Features**:
  - Browse available doctors
  - View doctor specializations
  - Book available appointment slots
  - View booking history
- **Booking System**:
  - Real-time slot availability
  - Race condition prevention (atomic transactions)
  - Automatic slot blocking after booking
- **Email Notifications** (Serverless):
  - Welcome emails on signup
  - Appointment confirmation emails

## 🛠️ Tech Stack

- **Backend**: Django 6.0.1
- **Database**: PostgreSQL
- **ORM**: Django ORM
- **Authentication**: Django built-in auth with custom User model
- **Email Service**: Serverless Framework (AWS Lambda-ready)
- **Version Control**: Git & GitHub

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Node.js 16+ (for Serverless Framework)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/shraddhamakam04/hospital-management-system.git
cd hospital-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Create PostgreSQL database:
```sql
CREATE DATABASE hospital_db;
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env` and update:
```bash
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=hospital_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## 📁 Project Structure
```
hospital-management-system/
├── core/                      # Main Django app
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   └── core/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── doctor_dashboard.html
│   │       ├── patient_dashboard.html
│   │       ├── create_availability.html
│   │       └── available_slots.html
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   └── email_service.py     # Email service helper
├── hospital_system/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── email_service/            # Serverless email function
│   ├── handler.py           # Lambda function handler
│   ├── serverless.yml       # Serverless configuration
│   └── requirements.txt     # Python dependencies
├── manage.py                 # Django management script
├── requirements.txt          # Project dependencies
├── .gitignore
└── README.md
```

## 🗄️ Database Schema

### User Model
- Custom user model extending AbstractUser
- Fields: username, email, password, role (doctor/patient)
- Related: DoctorProfile, PatientProfile

### DoctorProfile
- OneToOne with User
- Fields: specialization, phone

### PatientProfile
- OneToOne with User
- Fields: date_of_birth, phone

### AvailabilitySlot
- ForeignKey to User (doctor)
- Fields: date, start_time, end_time, is_booked
- Unique constraint: (doctor, date, start_time)

### Booking
- ForeignKey to User (patient)
- OneToOne with AvailabilitySlot
- Fields: booked_at, calendar_event_ids

## 🔐 Security Features

- Password hashing (Django PBKDF2)
- CSRF protection
- SQL injection prevention (ORM)
- Session-based authentication
- Environment variable protection (.env)
- Race condition prevention (select_for_update)

## 📧 Email Service (Serverless)

The email service is built using Serverless Framework and can be deployed to AWS Lambda.

### Local Testing
```bash
cd email_service
npm install
serverless offline start
```

### Supported Actions
- `SIGNUP_WELCOME`: Welcome email on registration
- `BOOKING_CONFIRMATION`: Appointment confirmation

## 🚀 Usage Guide

### For Doctors:
1. Sign up as a doctor
2. Login to doctor dashboard
3. Create availability slots (date, start time, end time)
4. View appointments when patients book

### For Patients:
1. Sign up as a patient
2. Login to patient dashboard
3. Browse available doctors
4. View doctor's available slots
5. Book an appointment
6. View booking history

## 🎯 Future Enhancements

- [ ] Google Calendar Integration
- [ ] Email notifications (live SMTP)
- [ ] Appointment cancellation
- [ ] Doctor ratings and reviews
- [ ] Medical history tracking
- [ ] Prescription management
- [ ] Payment integration
- [ ] SMS notifications
- [ ] Video consultation

## 👨‍💻 Developer

- **Name**: Shraddha Makam
- **GitHub**: [@shraddhamakam04](https://github.com/shraddhamakam04)
- **Email**: shraddhamakam04@gmail.com

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Django Documentation
- Serverless Framework
- PostgreSQL Community