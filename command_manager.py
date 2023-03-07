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
from paramiko import SSHClient

import logger

class CommandManager():
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
    def execute_command(cls, command: List[str]):
        """Execute command on remote server
        :param command:
            List of commands to execute on remote server
        """
        console_logger = logging.getLogger('connsole_output')
        # for cmd in command:
        #     console_logger.info(f'>>> {cmd}')
        #     proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #     for line in proc.stdout:
        #         if line != bytes():
        #             try:
        #                 line = line.decode().strip()
        #                 console_logger.info(f'{line}')
        #             except Exception as e:
        #                 console_logger.error(f'{e}')
        #     proc.wait()

        for cmd in command:
            stdin, stdout, stderr = cls.ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                console_logger.debug(
                    f"INPUT: {cmd}\n \
                    OUTPUT: {line}"
                )
            # time.sleep(0.3)


if __name__ == '__main__':
    Config.test_mode = True
    CommandManager.connect(use_pkey=True)
    CommandManager.execute_command(command=[
        f'mkdir test_remote_executing_command && cd $_; truncate -s {12}M {12}MB_largefile'
    ])