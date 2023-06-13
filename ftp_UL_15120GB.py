import io
import os
from ftplib import FTP
import random

# replace these with your FTP details
FTP_SERVER = 'localhost'
FTP_PORT = 2121  # replace with your port
FTP_USERNAME = 'ftp'
FTP_PASSWORD = 'ftp'

# data size in GB
DATA_SIZE_GB = 15120
# size of each chunk in MB
CHUNK_SIZE_MB = 10

# convert sizes to bytes
DATA_SIZE = DATA_SIZE_GB * 1024**3
CHUNK_SIZE = CHUNK_SIZE_MB * 1024**2

def upload_stream(ftp, stream, filename):
    # reset stream position to start
    stream.seek(0)
    # upload stream data
    ftp.storbinary(f'STOR {filename}', stream)

def connect_and_upload(server, port, username, password, data_size, chunk_size, filename):
    ftp = FTP()
    ftp.connect(server, port)
    ftp.login(username, password)

    bytes_sent = 0
    while bytes_sent < data_size:
        # generate random data for this chunk
        data = os.urandom(min(chunk_size, data_size - bytes_sent))
        # create a BytesIO object from the data
        stream = io.BytesIO(data)
        upload_stream(ftp, stream, filename)
        bytes_sent += len(data)

    ftp.quit()

if __name__ == "__main__":
    # replace this with your filename
    filename = 'data'
    connect_and_upload(FTP_SERVER, FTP_PORT, FTP_USERNAME, FTP_PASSWORD, DATA_SIZE, CHUNK_SIZE, filename)

