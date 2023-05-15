import subprocess
import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText

# GPIO pin numbers for each Raspberry Pi device
device_pins = {
    'pi1': 17,
    'pi2': 18,
    'pi3': 19,
    'pi4': 20,
    'pi5': 21
}

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
for pin in device_pins.values():
    GPIO.setup(pin, GPIO.OUT)

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

        # Wait for 1 minute before checking again
        time.sleep(60)

def send_email_notification():
    sender_email = 'your_email@gmail.com'  # Replace with your email address
    receiver_email = 'recipient_email@gmail.com'  # Replace with recipient's email address
    subject = 'Device Monitoring Complete'
    message = 'The device monitoring script has completed successfully.'

    # Create the email message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, 'your_email_password')  # Replace with your email password
        smtp.send_message(msg)

try:
    monitor_devices()
    send_email_notification()
except KeyboardInterrupt:
    GPIO.cleanup()
