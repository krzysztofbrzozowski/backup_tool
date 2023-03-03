"""
@author:    Krzysztof Brzozowski
@file:      main
@time:      03/03/2023
@desc:      
"""

from paramiko import SSHClient
from scp import SCPClient

from private_file import *

source = SOURCE
target = TARGET
# SSH/SCP Directory Recursively
# def ssh_scp_files(ssh_host, ssh_user, ssh_password, ssh_port, source_volume, destination_volume):

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname=HOST, username=USER, key_filename=PKEY, passphrase=PASSPHRASE)

with SCPClient(ssh.get_transport()) as scp:
    scp.get(remote_path=source, local_path=target)


if __name__ == '__main__':
    pass