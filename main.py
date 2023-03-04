"""
@author:    Krzysztof Brzozowski
@file:      main
@time:      03/03/2023
@desc:      
"""

from paramiko import SSHClient
from scp import SCPClient
import sys

from private_file import *

source = SOURCE
target = TARGET
# SSH/SCP Directory Recursively
# def ssh_scp_files(ssh_host, ssh_user, ssh_password, ssh_port, source_volume, destination_volume):


# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    progress = float(sent) / float(size) * 100
    print(f'{filename} progress: {progress:.2f}%')


class FileManager:
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=HOST, username=USER, key_filename=PKEY, passphrase=PASSPHRASE)

    @classmethod
    def get(cls):
        with SCPClient(transport=cls.ssh.get_transport(), progress=progress) as scp:
            scp.get(remote_path=source, local_path=target)


if __name__ == '__main__':
    FileManager.get()