"""
@author:    Krzysztof Brzozowski
@file:      main
@time:      03/03/2023
@desc:      
"""
import logging
import os
import stat
import time
import yaml

from pathlib import Path
from typing import List
from scp import SCPClient

# Private imports
from command_manager import CommandManager
from display_manager import DisplayManager


class FileManager(CommandManager):
    @staticmethod
    def create_dir(path: Path):
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except OSError as e:
            logging.error(e)

    @classmethod
    def get(cls, source_path: str | List[str], target_path: str, skip_path: str | List[str] = []):
        """Download file or directory from server
        :param source_path:
            Single or list of paths to download
        :param target_path:
            Destination path where downloaded files will be stored
        :param skip_path:
            Optional argument, when provided listened paths will be skipped during downloading
        :return:
            Downloaded target size, average download speed
        """
        CommandManager.connect(use_pkey=True)

        with SCPClient(transport=cls.ssh.get_transport(), progress=DisplayManager.progress) as scp:
            try:
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
                        # Dict structure {'path/to/file': True | False (recursive)}
                        _listdir = {os.path.join(source, file_name): stat.S_ISDIR(sftp.lstat(os.path.join(source, file_name)).st_mode)
                                    # Get list of all files
                                    for file_name in sftp.listdir(source)
                                    if os.path.join(source, file_name) not in skip_path}

                        # Target path will be one folder up (cd ..), name taken form source
                        _target_path = Path(os.path.join(target_path, source.split('/')[-1]))
                        cls.create_dir(path=_target_path)

                    # If source is file, verify if not in skipped path
                    else:
                        _listdir = {source: False} if source not in skip_path else None
                        _target_path = target_path

                    # Skip loop if empty list
                    if _listdir is None:
                        continue

                    # Start download
                    for _source, _recursive in _listdir.items():
                        scp.get(remote_path=_source, local_path=_target_path, recursive=_recursive)

            except Exception as e:
                logging.error(e)

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
    def get_backup_positions(cls):
        """Reads out desired backup sources from YAML config
        :return:
            Paths for files/directories to download, paths to omitting files/directories
        """
        with open(os.path.join(os.getenv('BACKUP_TOOL_DIR', None), 'config', 'backup_source_private.yaml'), 'r') as file:
            backup_paths = yaml.safe_load(file)
        return backup_paths['backup_source'], backup_paths['backup_source_skip']
