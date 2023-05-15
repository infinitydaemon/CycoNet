import subprocess
import RPi.GPIO as GPIO
import time

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

try:
    monitor_devices()
except KeyboardInterrupt:
    GPIO.cleanup()
