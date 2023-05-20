import subprocess

def test_bufferbloat(target_host, num_packets):
    # Run ping command to measure latency
    ping_cmd = ['ping', '-c', str(num_packets), target_host]
    ping_process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_output, ping_error = ping_process.communicate()

    if ping_error:
        print(f"Error running ping command: {ping_error.decode()}")
        return

    # Parse ping output to extract latency values
    ping_lines = ping_output.decode().splitlines()
    latencies = []
    for line in ping_lines:
        if "time=" in line:
            latency_str = line.split("time=")[-1].split()[0]
            latency_ms = float(latency_str)
            latencies.append(latency_ms)

    # Calculate average latency
    if len(latencies) > 0:
        avg_latency = sum(latencies) / len(latencies)
        print(f"Average latency to {target_host}: {avg_latency} ms")
    else:
        print(f"No latency data received from {target_host}")


# Example usage
target = "www.google.com"
num_packets = 10
test_bufferbloat(target, num_packets)
