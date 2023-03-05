"""
@author:    Krzysztof Brzozowski
@file:      config_manager
@time:      05/03/2023
@desc:      Deliver paths per setting written in config
"""
import platform
import yaml
import os


class ConfigManager:
    self_name = platform.node()
    config_path = os.path.join(os.getenv('BACKUP_TOOL_DIR', None), 'config', 'config_backup_tool_private.yaml')

    @classmethod
    def get_config(cls, test_mode=False):
        with open(cls.config_path, 'r') as file:
            config = yaml.safe_load(file)

        if test_mode:
            return config['TEST_USER']
        return config[cls.self_name]


if __name__ == '__main__':
    ConfigManager.get_config()
    pass

