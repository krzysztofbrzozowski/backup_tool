"""
@author:    Krzysztof Brzozowski
@file:      main
@time:      03/03/2023
@desc:      
"""
import sys
import time

from scp import SCPClient
import logging
import os
import yaml
from pathlib import Path
from typing import List
import stat

from command_manager import CommandManager
from display_manager import DisplayManager


class FileManager(CommandManager):
    start = None
    chunk = None

    @classmethod
    def get(cls, source_path: str | List[str], target_path: str, skip_path: str | List[str] = None, recursive=False):
        """Download file from server
        :param skip_path:
        :param source_path:
        :param target_path:
        :param recursive:
        :return:
        """
        CommandManager.connect(use_pkey=True)

        # TODO put that in try (if one path fail, another might be downloaded)
        with SCPClient(transport=cls.ssh.get_transport(), progress=DisplayManager.progress) as scp:
            # Init SFTP client
            sftp = cls.ssh.open_sftp()

            # Start measure
            start_time = time.time()

            # Change to list if one path is provided
            if isinstance(source_path, str):
                source_path = [source_path]

            # Select paths which are not marked as skipped and download
            for source in source_path:
                _lstat = sftp.lstat(source)
                # If source is directory, get all sub dirs and files it contains
                if stat.S_ISDIR(_lstat.st_mode):
                    _listdir = [os.path.join(source, file_name) for file_name
                                # Get list of all files
                                in sftp.listdir(source)
                                if os.path.join(source, file_name) not in skip_path]

                # If source is file, verify if not in skipped path
                else:
                    _listdir = [source] if source not in skip_path else None

                # Skip loop if empty list
                if _listdir is None:
                    continue

                # Start download
                for _source in _listdir:
                    scp.get(remote_path=_source, local_path=target_path, recursive=False)

        # Calculate file size for file or folder
        target = Path(target_path)
        if os.path.isfile(target):
            target_size = os.stat(target).st_size
        if os.path.isdir(target):
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
