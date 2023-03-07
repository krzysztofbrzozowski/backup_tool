"""
@author:    Krzysztof Brzozowski
@file:      command_manager
@time:      07/03/2023
@desc:      
"""
import subprocess
import logging


class CommandManager:
    def execute_commands(self, commands: List[str]):
        """
        """

        for command in commands:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in proc.stdout:
                if line != bytes():
                    try:
                        line = line.decode().strip()
                        logging.info(f'{command=} {line=}')
                    except Exception as e:
                        logging.error(f'{e}')
            proc.wait()