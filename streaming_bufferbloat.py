import subprocess
import time

def test_bufferbloat(target_host, num_packets):
    ping_cmd = ['ping', '-c', str(num_packets), target_host]
    ping_process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_output, ping_error = ping_process.communicate()

    if ping_error:
        print(f"Error running ping command: {ping_error.decode()}")
        return
      
    ping_lines = ping_output.decode().splitlines()
    latencies = []
    for line in ping_lines:
        if "time=" in line:
            latency_str = line.split("time=")[-1].split()[0]
            latency_ms = float(latency_str)
            latencies.append(latency_ms)

    if len(latencies) > 0:
        avg_latency = sum(latencies) / len(latencies)
        print(f"Average latency to {target_host}: {avg_latency} ms")
    else:
        print(f"No latency data received from {target_host}")

    # Run video streaming test
    video_url = "http://example.com/video.mp4"  # Replace with the actual video URL
    start_time = time.time()
    download_cmd = ['ffmpeg', '-i', video_url, '-f', 'null', '-']
    download_process = subprocess.Popen(download_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    download_process.communicate()
    end_time = time.time()
    download_time = end_time - start_time
    print(f"Video streaming test completed. Download time: {download_time} seconds")

# Example usage
target = "www.example.com"
num_packets = 10
test_bufferbloat(target, num_packets)
