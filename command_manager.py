"""
@author:    Krzysztof Brzozowski
@file:      command_manager
@time:      07/03/2023
@desc:      
"""
import sys
import subprocess
import logging
import time
from typing import List

from config_manager import ConfigManager as Config
from paramiko import SSHClient, AutoAddPolicy

import logger


class CommandManager:
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
            cls.ssh.set_missing_host_key_policy(AutoAddPolicy())
            if use_pkey:
                # Logging with private key
                cls.ssh.connect(
                    hostname=Config.get_config_value('HOST'),
                    username=Config.get_config_value('USER'),
                    key_filename=Config.get_config_value('PKEY'),
                    passphrase=Config.get_config_value('PASSPHRASE'))

            # Logging with password
            cls.ssh.connect(
                hostname=Config.get_config_value('HOST'),
                username=Config.get_config_value('USER'),
                password=Config.get_config_value('PASSWD'))

        except BaseException as e:
            sys.exit(f'Unable to connect ot the server - {e}')

    @classmethod
    def close(cls):
        """Close SSH connection"""
        cls.ssh.close()

    @classmethod
    def execute_command(cls, command: str | List[str]):
        """Execute command on remote server
        :param command:
            List of commands to execute on remote server
        """
        console_logger = logging.getLogger('connsole_output')

        if isinstance(command, str):
            command = [command]

        for cmd in command:
            stdin, stdout, stderr = cls.ssh.exec_command(cmd, get_pty=True)
            for line in iter(stdout.readline, ""):
                console_logger.info(f'{cmd} -> {line}')


if __name__ == '__main__':
    logging.disable(logging.DEBUG)

    Config.test_mode = True
    CommandManager.connect(use_pkey=True)

    expected_random_size = 3
    CommandManager.execute_command(command=[
        f'cd {Config.get_config_value("TEST_DIR_SOURCE")} ; rm -r test_remote_executing_command',
        f'cd {Config.get_config_value("TEST_DIR_SOURCE")} ; mkdir test_remote_executing_command',
        f'cd {Config.get_config_value("TEST_DIR_SOURCE")}/test_remote_executing_command ; truncate -s {expected_random_size}M {expected_random_size}MB_largefile'
        f'cd {Config.get_config_value("TEST_DIR_SOURCE")}/test_remote_executing_command ; ls -al'
    ])

