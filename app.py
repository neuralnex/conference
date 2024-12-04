from flask import Flask, render_template, request, redirect, url_for, flash
import random
import string
import requests
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Replace with a strong secret key

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'  # For Gmail
SMTP_PORT = 587  # For TLS
SENDER_EMAIL = os.getenv('SENDER_EMAIL')  # Your email address
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')  # Your email password

def generate_ticket_id(length=8):
    """Generate a random ticket ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_email(to, subject, body):
    """Send an email using SMTP."""
    # Create the email content
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = to

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in to the server
            server.sendmail(SENDER_EMAIL, to, message.as_string())  # Send the email
        print('Email sent successfully!')
    except Exception as e:
        print(f'An error occurred: {e}')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        home_phone = request.form.get('home_phone')
        state = request.form.get('state')
        email = request.form.get('email')
        department = request.form.get('department')
        address = request.form.get('address')
        attendance = request.form.get('attendance')
        reason = request.form.get('reason')

        # Generate a random ticket ID
        ticket_id = generate_ticket_id()

        # Create and send the email
        subject = 'Your Ticket ID'
        body = f"Hello {first_name} {last_name},\n\nYour ticket ID is: {ticket_id}\n\nThank you for registering!"
        send_email(email, subject, body)

        # Prepare data to send to Google Sheets
        data = [first_name, last_name, home_phone, state, email, department, address, attendance, reason, ticket_id]
        
        # Send data to Google Sheets
        google_sheets_url = "https://script.google.com/macros/s/AKfycbx6F5lU-DS_ffwhnOSa3rRFwfAKAwdaNxWl-jeuKSWonA6yNy5IUJf4ySPAuxm-11Cj/exec"  # Replace with your actual web app URL
              # Send data to Google Sheets
        response = requests.post(google_sheets_url, data={
            'first-name': first_name,
            'last-name': last_name,
            'phone': home_phone,
            'state': state,
            'email': email,
            'department': address,
            'address': address,
            'attendance': attendance,
            'reason': reason
        })

        flash('Registration successful! A ticket ID has been sent to your email.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/speakers')
def speakers():
    return render_template('speakers.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

if __name__ == '__main__':
    app.run(debug=True)