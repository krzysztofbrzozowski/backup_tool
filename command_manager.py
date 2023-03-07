"""
@author:    Krzysztof Brzozowski
@file:      command_manager
@time:      07/03/2023
@desc:      
"""
import sys
import subprocess
import logging
from typing import List

from config_manager import ConfigManager as Config
from paramiko import SSHClient


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

    # def execute_command(cls, commands: List[str]):
    #     """
    #     """
    #     cls.ssh.exec_command()
    #     # for command in commands:
    #     #     proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #     #
    #     #     for line in proc.stdout:
    #     #         if line != bytes():
    #     #             try:
    #     #                 line = line.decode().strip()
    #     #                 logging.info(f'{command=} {line=}')
    #     #             except Exception as e:
    #     #                 logging.error(f'{e}')
    #     #     proc.wait()
