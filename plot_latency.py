import subprocess
import matplotlib.pyplot as plt

def measure_latency(target_host, num_packets):

    ping_cmd = ['ping', '-c', str(num_packets), target_host]
    ping_process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_output, ping_error = ping_process.communicate()

    if ping_error:
        print(f"Error running ping command: {ping_error.decode()}")
        return None

    ping_lines = ping_output.decode().splitlines()
    latencies = []
    for line in ping_lines:
        if "time=" in line:
            latency_str = line.split("time=")[-1].split()[0]
            latency_ms = float(latency_str)
            latencies.append(latency_ms)

    return latencies

target = "www.google.com"
num_packets = 10
latency_data = measure_latency(target, num_packets)

# Plotting the latency graph
if latency_data:
    plt.plot(latency_data, 'o-')
    plt.xlabel("Packet Number")
    plt.ylabel("Latency (ms)")
    plt.title("Network Latency")
    plt.grid(True)
    plt.show()
