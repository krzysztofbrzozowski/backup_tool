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
from display_manager import DisplayManager

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

    @classmethod
    def get(cls, source_path: str, target_path: str):
        with SCPClient(transport=cls.ssh.get_transport(), progress=DisplayManager.progress) as scp:
            # Start measure
            start_time = time.time()
            # cls.start = time.time()
            # cls.chunk = 0
            # Start download
            scp.get(remote_path=source_path, local_path=target_path)

        # MB size by default on OSX
        target_size = os.stat(target_path).st_size
        # Download speed calculated as: file size / time to download
        avg_download_speed = target_size / (time.time() - start_time)
        print(f'{avg_download_speed:.2f}MB/s')


if __name__ == '__main__':
    FileManager.connect()
    FileManager.get(source_path=SOURCE, target_path=TARGET)