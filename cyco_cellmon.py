# Monitor a CycoNet Android cell monitor's status using ADB

import subprocess
import time

def run_adb_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode().strip()

def monitor_android_device():
    # Check if ADB is installed and accessible
    output = run_adb_command(['adb', 'version'])
    if not output.startswith('Android Debug Bridge'):
        print("ADB is not installed or accessible.")
        return

    # Get connected devices
    output = run_adb_command(['adb', 'devices'])
    devices = [line.split('\t')[0] for line in output.splitlines()[1:] if line.endswith('\tdevice')]

    if not devices:
        print("No Android devices are connected.")
        return

    # Monitor the first connected device
    device = devices[0]

    while True:
        # Get battery level
        battery_level = run_adb_command(['adb', '-s', device, 'shell', 'dumpsys', 'battery', '|', 'grep', '-E', '"level"'])
        print("Battery Level:", battery_level)

        # Get device temperature
        temperature = run_adb_command(['adb', '-s', device, 'shell', 'dumpsys', 'battery', '|', 'grep', '-E', '"temperature"'])
        print("Device Temperature:", temperature)

        # Get CPU usage
        cpu_info = run_adb_command(['adb', '-s', device, 'shell', 'top', '-n', '1', '-d', '1', '|', 'grep', '"%cpu"'])
        print("CPU Usage:", cpu_info)

        # Get memory usage
        mem_info = run_adb_command(['adb', '-s', device, 'shell', 'dumpsys', 'meminfo'])
        print("Memory Usage:", mem_info)

        # Sleep for 5 seconds
        time.sleep(5)

if __name__ == '__main__':
    monitor_android_device()
