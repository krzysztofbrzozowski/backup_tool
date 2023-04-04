"""
@author:    Krzysztof Brzozowski
@file:      config_manager
@time:      05/03/2023
@desc:      Deliver paths per setting written in config
"""
import logging
import os
import yaml
import platform
from pathlib import Path

from typing import List


class ConfigManager:
    # If test_mode selected it will take TEST_USER config from the YAML
    test_mode = False
    self_name = platform.node()

    # Change this line if needed
    # config_path = os.path.join(os.getenv('BACKUP_TOOL_DIR', None), 'config', 'config_backup_tool_private.yaml')

    # This statement will work until 'tests' dir has the same parent as 'config' dir (parent 'backup_tool' dir)
    config_path = os.path.join(
        Path(__file__).parent,
        'config', 'config_backup_tool_private.yaml')

    @classmethod
    def get_config(cls):
        """Reads YAML config form selected file
        :return:
            Return read config with automatically chosen user
        """
        with open(cls.config_path, 'r') as file:
            config = yaml.safe_load(file)

        if cls.test_mode:
            return config['TEST_USER']
        return config[cls.self_name]

    @classmethod
    def get_config_value(cls, config_key: str = None):
        """Reads YAML config with selected key"""
        try:
            return cls.get_config()[config_key]
        except KeyError as e:
            logging.error(e)

    @classmethod
    def get_config_values(cls, config_keys: List[str] = None):
        """Reads YAML config with selected key"""
        try:
            return [cls.get_config()[config_key] for config_key in config_keys]
        except KeyError as e:
            logging.error(e)


if __name__ == '__main__':
    ConfigManager.get_config_value('USER')
    pass

