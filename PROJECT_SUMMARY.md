# Hospital Management System - Project Summary

## Student Information
- **Name**: Shraddha Makam
- **Email**: shraddhamakam04@gmail.com
- **Project**: Mini Hospital Management System
- **Completion Date**: January 15, 2026

## Project Overview
A full-stack web application for managing hospital appointments with doctor availability scheduling, patient booking system, and serverless email notifications.

## Technologies Used

### Backend
- **Framework**: Django 6.0.1
- **Language**: Python 3.12.4
- **Database**: PostgreSQL
- **ORM**: Django ORM

### Serverless
- **Framework**: Serverless Framework
- **Runtime**: Python 3.9
- **Platform**: AWS Lambda (configured)
- **Email**: SMTP integration

### Version Control
- **Git**: 2.52.0
- **Repository**: GitHub
- **URL**: https://github.com/shraddhamakam04/hospital-management-system

## Features Implemented

### ✅ Authentication System
- Custom User model with role-based access (Doctor/Patient)
- Secure password hashing
- Session-based authentication
- Role-specific dashboards

### ✅ Doctor Features
- Register and login
- Create availability time slots
- View all created slots
- See booking status (Available/Booked)
- View all appointments with patient details

### ✅ Patient Features
- Register and login
- Browse all available doctors
- View doctor specializations
- See available time slots
- Book appointments
- View booking history

### ✅ Booking System
- Real-time availability checking
- Atomic transactions (race condition prevention)
- Automatic slot blocking
- One slot per booking constraint
- Future date validation

### ✅ Serverless Email Service
- Separate microservice architecture
- Welcome email on signup
- Booking confirmation emails
- SMTP integration ready
- Serverless Framework configuration

### ✅ Database Design
- Custom User model
- DoctorProfile (one-to-one)
- PatientProfile (one-to-one)
- AvailabilitySlot (with unique constraints)
- Booking (with relationships)

### ✅ Security
- Password hashing (PBKDF2)
- CSRF protection
- Environment variable management
- SQL injection prevention
- Proper authentication checks

## Technical Achievements

1. **Custom User Model**: Extended Django's AbstractUser for role-based access
2. **Transaction Management**: Used atomic transactions to prevent booking conflicts
3. **Microservices**: Separated email service as independent serverless function
4. **Database Constraints**: Implemented unique constraints for data integrity
5. **Git Workflow**: Regular commits with meaningful messages

## Files & Structure

### Core Application Files
- `core/models.py` - Database models (5 models)
- `core/views.py` - Business logic (9 views)
- `core/forms.py` - User input forms (3 forms)
- `core/urls.py` - URL routing (9 routes)
- `core/email_service.py` - Email integration helper

### Templates (8 files)
- base.html, home.html, login.html, signup.html
- doctor_dashboard.html, patient_dashboard.html
- create_availability.html, available_slots.html

### Serverless Service
- `email_service/handler.py` - Lambda function
- `email_service/serverless.yml` - Configuration
- Support for AWS Lambda deployment

## Database Schema

**5 Models Created:**
1. User (custom, extends AbstractUser)
2. DoctorProfile
3. PatientProfile
4. AvailabilitySlot
5. Booking

**Relationships:**
- One-to-One: User ↔ DoctorProfile
- One-to-One: User ↔ PatientProfile
- One-to-Many: Doctor → AvailabilitySlots
- One-to-Many: Patient → Bookings
- One-to-One: AvailabilitySlot ↔ Booking

## Git Commits
- Initial setup and configuration
- Database models and migrations
- Views and templates implementation
- Email service integration
- Documentation

## Testing Performed

### Manual Testing
✅ Doctor signup and login
✅ Patient signup and login
✅ Creating availability slots
✅ Viewing available doctors
✅ Booking appointments
✅ Slot blocking after booking
✅ Dashboard data display
✅ Role-based access control

## Known Limitations

1. **Email Service**: Configured but not sending live emails (placeholder SMTP credentials)
2. **Google Calendar**: Not implemented (optional feature)
3. **Deployment**: Local development only, not deployed to production

## Future Improvements

- Implement Google Calendar API integration
- Add appointment cancellation feature
- Enable live email notifications
- Add search and filter functionality
- Implement appointment reminders
- Add doctor ratings and reviews

## Lessons Learned

1. Database design and relationships
2. Django ORM and migrations
3. User authentication and authorization
4. Transaction management for data integrity
5. Git version control best practices
6. Serverless architecture concepts
7. Full-stack development workflow

## Conclusion

Successfully built a functional hospital management system with all core requirements:
- ✅ Doctor and patient registration
- ✅ Availability management
- ✅ Appointment booking
- ✅ Database design and implementation
- ✅ Serverless email service structure
- ✅ Git version control
- ✅ Professional documentation

The system is fully operational for local demonstration and ready for presentation.