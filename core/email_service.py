import requests
import os

SERVERLESS_EMAIL_URL = os.getenv('SERVERLESS_EMAIL_URL', 'http://localhost:3000/dev/send-email')

def send_email(action, to_email, data):
    """
    Send email via serverless function
    action: 'SIGNUP_WELCOME' or 'BOOKING_CONFIRMATION'
    """
    payload = {
        'action': action,
        'to': to_email,
        'data': data
    }
    
    try:
        response = requests.post(SERVERLESS_EMAIL_URL, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Email service error: {e}")
        return False