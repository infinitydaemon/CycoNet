# Monitor a particular device for realtime log analysis from CycoNet
import paramiko
import time

# SSH connection settings
host = 'your_host'
username = 'your_username'
password = 'your_password'

# Command to retrieve kernel logs
kernel_log_command = 'tail -n 10 /var/log/kern.log'

# Command to retrieve system logs
system_log_command = 'tail -n 10 /var/log/syslog'

def ssh_login(host, username, password):
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote host
    client.connect(host, username=username, password=password)

    return client

def retrieve_logs(ssh_client, command):
    # Execute command and retrieve logs
    _, stdout, _ = ssh_client.exec_command(command)
    logs = stdout.readlines()
    return logs

def display_logs(logs):
    # Display logs on the terminal
    print('=== Logs ===')
    for log in logs:
        print(log.strip())
    print()

# SSH login
ssh_client = ssh_login(host, username, password)

try:
    while True:
        # Retrieve and display kernel logs
        kernel_logs = retrieve_logs(ssh_client, kernel_log_command)
        display_logs(kernel_logs)

        # Retrieve and display system logs
        system_logs = retrieve_logs(ssh_client, system_log_command)
        display_logs(system_logs)

        # Wait for 10 seconds before refreshing
        time.sleep(10)

except KeyboardInterrupt:
    # Close SSH connection on keyboard interrupt
    ssh_client.close()
