import subprocess
import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# GPIO and device monitoring code here...

def send_email_notification():
    sender_email = 'your_email@your_domain.com'  # Replace with your email address
    receiver_email = 'recipient_email@recipient_domain.com'  # Replace with recipient's email address
    subject = 'Device Monitoring Complete'
    message = 'The device monitoring script has completed successfully.'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Configure the SMTP server
    smtp_server = 'smtp.your_domain.com'  # Replace with your SMTP server address
    smtp_port = 587  # Replace with your SMTP server port
    smtp_username = 'your_smtp_username'  # Replace with your SMTP username
    smtp_password = 'your_smtp_password'  # Replace with your SMTP password

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)

try:
    monitor_devices()
    send_email_notification()
except KeyboardInterrupt:
    GPIO.cleanup()
