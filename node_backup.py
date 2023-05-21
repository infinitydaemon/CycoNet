import paramiko

def ssh_login(hostname, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(hostname, port=port, username=username, password=password)
        print("SSH login successful.")
        return ssh_client
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_exception:
        print(f"SSH connection failed: {str(ssh_exception)}")
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Unable to connect to the SSH server.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return None

def take_sdcard_backup(ssh_client, destination_path):
    try:
        stdin, stdout, stderr = ssh_client.exec_command("sudo dd if=/dev/mmcblk0 of=/home/gateway/sdcard_backup.img bs=4M") # Replace with the default user dir.
        exit_status = stdout.channel.recv_exit_status() # The default factory set user varies from node to node. For WiFi AP, default user is cwdsystems.

        if exit_status == 0:
            print("MicroSD card backup completed.")
            sftp_client = ssh_client.open_sftp()
            sftp_client.get("/home/gateway/sdcard_backup.img", destination_path)
            sftp_client.close()
            print(f"Backup downloaded to {destination_path}")
        else:
            print("Error occurred during backup process.")

    except Exception as e:
        print(f"An error occurred during backup: {str(e)}")

def main():
    hostname = "gateway"  # Replace with the actual hostname or IP address of the node.
    port = 22  # Default SSH port
    username = "gateway"  # Replace with the factory set username
    password = "password"  # Replace with the actual password
    destination_path = "/path/to/save/backup.img"  # Replace with the desired destination path on your local computer.
    # Alter the path based on distro or operating system type.

    ssh_client = ssh_login(hostname, port, username, password)
    if ssh_client:
        take_sdcard_backup(ssh_client, destination_path)
        ssh_client.close()

if __name__ == "__main__":
    main()
