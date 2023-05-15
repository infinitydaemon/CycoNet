import subprocess
import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# GPIO and device monitoring code here...

def check_reachability(ip):
    result = subprocess.call(['ping', '-c', '1', ip])
    return result == 0

def monitor_devices():
    while True:
        for device, pin in device_pins.items():
            # Check reachability
            ip = f'192.168.1.{device[-1]}'  # Example IP address pattern
            reachable = check_reachability(ip)

            # Check power status
            powered_on = GPIO.input(pin) == GPIO.HIGH

            # Take action based on device status
            if not reachable and powered_on:
                # Power off the device
                GPIO.output(pin, GPIO.LOW)
                print(f'{device} powered off.')
            elif reachable and not powered_on:
                # Power on the device
                GPIO.output(pin, GPIO.HIGH)
                print(f'{device} powered on.')

        # Wait for 5 minutes before checking again
        time.sleep(300)

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
    while True:
        monitor_devices()
        send_email_notification()
except KeyboardInterrupt:
    GPIO.cleanup()
