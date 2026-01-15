import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(event, context):
    """
    Serverless function to send emails
    """
    try:
        # Parse the request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        action = body.get('action')
        to_email = body.get('to')
        data = body.get('data', {})
        
        # Email configuration from environment variables
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        # Create email content based on action
        if action == 'SIGNUP_WELCOME':
            subject = 'Welcome to Hospital Management System'
            html_content = f"""
            <html>
                <body>
                    <h2>Welcome {data.get('name', 'User')}!</h2>
                    <p>Thank you for signing up as a {data.get('role', 'user')}.</p>
                    <p>You can now access all features of our Hospital Management System.</p>
                    <br>
                    <p>Best regards,<br>HMS Team</p>
                </body>
            </html>
            """
        
        elif action == 'BOOKING_CONFIRMATION':
            subject = 'Appointment Confirmation'
            html_content = f"""
            <html>
                <body>
                    <h2>Appointment Confirmed!</h2>
                    <p>Dear {data.get('patient_name', 'Patient')},</p>
                    <p>Your appointment has been successfully booked:</p>
                    <ul>
                        <li><strong>Doctor:</strong> {data.get('doctor_name', 'N/A')}</li>
                        <li><strong>Date:</strong> {data.get('date', 'N/A')}</li>
                        <li><strong>Time:</strong> {data.get('time', 'N/A')}</li>
                    </ul>
                    <p>Please arrive 10 minutes before your appointment time.</p>
                    <br>
                    <p>Best regards,<br>HMS Team</p>
                </body>
            </html>
            """
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid action'})
            }
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = smtp_username
        message['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Email sent successfully',
                'action': action
            })
        }
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }