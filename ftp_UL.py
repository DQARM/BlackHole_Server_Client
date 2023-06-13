import io
import os
import socket
import argparse
import time
import random
from ftplib import FTP
from datetime import datetime

class CustomFTP(FTP):
    def __init__(self, source_address, *args, **kwargs):
        self.source_address = source_address
        super().__init__(*args, **kwargs)

    def connect(self, host='', port=0, timeout=30, source_address=None):
        if source_address is None:
            source_address = self.source_address

        self.sock = socket.create_connection((host, port), timeout, source_address)
        self.af = self.sock.family
        self.file = self.sock.makefile('r')
        self.welcome = self.getresp()
        return self.welcome

# Parse command line arguments
parser = argparse.ArgumentParser(description='FTP client, it will upload a file to FTP Server')
parser.add_argument('--server_ip', required=True, help='Server IP address')
parser.add_argument('--server_port', type=int, default=21, help='Server port')
parser.add_argument('--source_ip', default=None, help='Source IP address')
parser.add_argument('--username', default='ftp', help='Username')
parser.add_argument('--password', default='ftp', help='Password')
parser.add_argument('--logfile',  help='Log file name')
parser.add_argument('--filesize_gb', type=int, default=15120, help='File size to upload in GB')

args = parser.parse_args()

# Calculate total bytes to send
total_bytes_to_send = args.filesize_gb * 1024**3  # 1GB is 1024**3 bytes

# Initialize FTP
ftp = CustomFTP(source_address=(args.source_ip, 0) if args.source_ip else None)
ftp.connect(args.server_ip, args.server_port)
ftp.login(args.username, args.password)

# Send data
sent_bytes = 0
start_time = time.time()
bytes_sent_in_current_second = 0
total_time = 0

# Check if logfile already exists, if so, append a timestamp and a random suffix
logfile = args.logfile if args.logfile else "FTP_UL"
logfile = logfile + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random.randint(1000, 9999)) + ".txt"

# Open the file to write speeds
try:
    with open(logfile, 'w') as log_file:
        # Log start time, server IP, server port, source IP (if set), and file size
        log_file.write(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Server IP: {args.server_ip}\n")
        log_file.write(f"Server port: {args.server_port}\n")
        if args.source_ip:
            log_file.write(f"Source IP: {args.source_ip}\n")
        log_file.write(f"File size: {args.filesize_gb} GB\n")

        while sent_bytes < total_bytes_to_send:
            # Generate a random payload of 1 MB at a time
            payload_size_bytes = min(1024**2, total_bytes_to_send - sent_bytes)
            payload = os.urandom(payload_size_bytes)

            # Upload payload
            with io.BytesIO(payload) as payload_io:
                ftp.storbinary(f'STOR data.bin', payload_io)

            # Update sent bytes
            sent_bytes += payload_size_bytes
            bytes_sent_in_current_second += payload_size_bytes

            # Check if a second has passed since we last logged speed
            if int(time.time()) > start_time + total_time:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}      Uploading...")
                #print(f"Upload speed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {bytes_sent_in_current_second} bytes/sec")
                log_file.write(f"Upload speed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {bytes_sent_in_current_second} bytes/sec\n")
                log_file.flush()
                
                total_time += 1
                bytes_sent_in_current_second = 0
except KeyboardInterrupt:
    pass

average_speed = sent_bytes / total_time if total_time > 0 else 0
with open(logfile, 'a') as log_file:
    log_file.write(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write(f"Average upload speed: {average_speed} bytes/sec\n")
    log_file.flush()

ftp.quit()

