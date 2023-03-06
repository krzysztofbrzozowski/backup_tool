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
import logging
import os
import yaml
from pathlib import Path

from display_manager import DisplayManager
from config_manager import ConfigManager as Config


class FileManager:
    start = None
    chunk = None
    ssh = SSHClient()

    @classmethod
    def connect(cls, use_pkey=True):
        """Connect to server via SSH using private key
        :param use_pkey:
            If selected, will load local private keys form folder
        :return:
            None if successfully connected
        :raises:
            Exception if unable to connect to server
        """
        logging.info('SSH connceting')
        if use_pkey:
            cls.ssh.load_system_host_keys()

        try:
            cls.ssh.connect(
                hostname=Config.get_config_value('HOST'),
                username=Config.get_config_value('USER'),
                key_filename=Config.get_config_value('PKEY'),
                passphrase=Config.get_config_value('PASSPHRASE'))
        except BaseException as e:
            sys.exit(f'Unable to connect ot the server - {e}')

    @classmethod
    def close(cls):
        """Close SSH connection"""
        cls.ssh.close()

    @classmethod
    def get(cls, source_path: str, target_path: str, recursive=False):
        """Download file from server
        :param source_path:
        :param target_path:
        :param recursive:
        :return:
        """
        with SCPClient(transport=cls.ssh.get_transport(), progress=DisplayManager.progress) as scp:
            # Start measure
            start_time = time.time()
            # cls.start = time.time()
            # cls.chunk = 0
            # Start download
            scp.get(recursive=recursive, remote_path=source_path, local_path=target_path)

        # Calculate file size for folder
        target = Path(target_path)
        target_size = sum(f.stat().st_size for f in target.glob('**/*') if f.is_file())
        # Download speed calculated as: file size / time to download
        avg_download_speed = (target_size / (1024 * 1024)) / (time.time() - start_time)
        logging.info(f'{avg_download_speed:.2f}MB/s')

        return target_size, avg_download_speed

    @classmethod
    def put(cls, source_path: str, target_path: str, recursive=False):
        """Upload file or files to remote path
        :param source_path:
        :param target_path:
        :param recursive:
        :return:
        """
        with SCPClient(transport=cls.ssh.get_transport(), progress=DisplayManager.progress) as scp:
            # Start measure
            start_time = time.time()
            # Start upload
            scp.put(recursive=recursive, remote_path=target_path, files=source_path)

    @classmethod
    def get_backup_positions(cls):
        with open(os.path.join(os.getenv('BACKUP_TOOL_DIR', None), 'config', 'backup_source.yaml'), 'r') as file:
            backup_paths = yaml.safe_load(file)
        return backup_paths['backup_source']
