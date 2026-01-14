# Hospital Management System

A mini hospital management web application with doctor availability management, patient appointment booking, and serverless email notifications.

## Tech Stack
- Backend: Django 6.0
- Database: PostgreSQL
- Email Service: Serverless Framework (AWS Lambda)
- APIs: Google Calendar API

## Features
- Doctor and Patient authentication
- Doctor availability management  
- Patient appointment booking
- Google Calendar integration
- Email notifications via serverless function

## Setup Instructions

### Prerequisites
- Python 3.12+
- PostgreSQL
- Node.js

### Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update with your values
6. Create PostgreSQL database named `hospital_db`
7. Run migrations: `python manage.py migrate`
8. Start server: `python manage.py runserver`

## Project Structure
```
HospitalProject/
├── core/              # Main Django app
├── hospital_system/   # Django project settings
├── email_service/     # Serverless email function
├── venv/              # Virtual environment
└── manage.py          # Django management script
```