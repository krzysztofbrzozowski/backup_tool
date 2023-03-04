"""
@author:    Krzysztof Brzozowski
@file:      main
@time:      03/03/2023
@desc:      
"""
import sys
import time

from paramiko import SSHClient
from scp import SCPClient
import os

from private_file import *

source = SOURCE
target = TARGET
# SSH/SCP Directory Recursively
# def ssh_scp_files(ssh_host, ssh_user, ssh_password, ssh_port, source_volume, destination_volume):


class FileManager:
    start = None
    chunk = None
    ssh = SSHClient()

    @classmethod
    def connect(cls, use_pkey=True):
        """Connect to server using private key
        :param use_pkey:
        :return: None if successfully connected
        :raises: Exception if unable to connect to server
        """
        if use_pkey:
            cls.ssh.load_system_host_keys()

        try:
            cls.ssh.connect(hostname=HOST, username=USER, key_filename=PKEY, passphrase=PASSPHRASE)
        except BaseException as e:
            sys.exit(f'Unable to connect ot the server - {e}')

    @classmethod
    def close(cls):
        cls.ssh.close()

    # Define progress callback that prints the current percentage completed for the file
    @classmethod
    def progress(cls, filename, size, sent):
        progress = float(sent) / float(size) * 100
        print(f'{filename} progress: {progress:.2f}%')

        print(f'MB total size = {size / (1024 * 1024)}')
        print(f'GB total size = {size / (1024 * 1024 * 1024)}')

        print(f'MB total sent = {sent / (1024 * 1024)}')
        print(f'GB total sent = {sent / (1024 * 1024 * 1024)}')

        chunk_diff = sent - cls.chunk
        chunk_diff = chunk_diff / (1024 * 1024)             # MB size
        print(f'chunk diff MB = {chunk_diff}')

        time_diff = time.time() - cls.start
        print(f'time diff = {time_diff}')

        # try:
        #     if time_diff < 1:
        #         time_diff = 1 / time_diff
        #
        # except ZeroDivisionError as e:
        #     print(e)

        # try:
        #     if chunk_diff < 1:
        #         chunk_diff = 1 / chunk_diff
        # except ZeroDivisionError as e:
        #     print(e)

        print(f'speed {chunk_diff * (1 / time_diff)} MB/s')

        cls.start = time.time()
        cls.chunk = sent

    @classmethod
    def get(cls):
        with SCPClient(transport=cls.ssh.get_transport(), progress=cls.progress) as scp:
            # Start measure
            avg_start = time.time()
            cls.start = time.time()
            cls.chunk = 0
            # Start download
            scp.get(remote_path=source, local_path=target)

        file_size = os.stat(target).st_size     # MB size
        download_time = time.time() - avg_start
        avg_download_speed = file_size / download_time

        print(f'{file_size=}MB / {download_time=}s')
        print(f'{avg_download_speed:.2f}MB/s')



if __name__ == '__main__':
    FileManager.connect(use_pkey=False)
    FileManager.get()