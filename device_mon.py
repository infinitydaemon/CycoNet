# Monitor a particular device for realtime log analysis from CycoNet
import paramiko
import time

def connect_ssh(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client

def get_kernel_logs(ssh_client):
    _, stdout, _ = ssh_client.exec_command('dmesg --ctime')
    kernel_logs = stdout.readlines()
    return kernel_logs[-40:]

def get_system_logs(ssh_client):
    _, stdout, _ = ssh_client.exec_command('journalctl --since "10 seconds ago"')
    system_logs = stdout.readlines()
    return system_logs

def print_logs(kernel_logs, system_logs):
    print("Last 40 Kernel Logs:")
    for log in kernel_logs:
        print(log.strip())
    print("\nLast System Logs:")
    for log in system_logs:
        print(log.strip())

def main():
    hostname = 'your_hostname'
    username = 'your_username'
    password = 'your_password'

    try:
        ssh_client = connect_ssh(hostname, username, password)
        while True:
            kernel_logs = get_kernel_logs(ssh_client)
            system_logs = get_system_logs(ssh_client)
            print_logs(kernel_logs, system_logs)
            time.sleep(10)
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as ssh_ex:
        print(f"An error occurred: {ssh_ex}")
    finally:
        if ssh_client:
            ssh_client.close()

if __name__ == '__main__':
    main()
