"""
@author:    Krzysztof Brzozowski
@file:      logger
@time:      04/03/2023
@desc:      Logger configuration allows read config from *.yaml file
            Added functionality to read out *.yaml config from sys env location
"""
import logging.config
import yaml
import os
import re

from pathlib import Path

# Added path loader to load environment variable from in YAML file
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)


class DebugFilter(logging.Filter):
    def filter(self, log_record):
        if log_record.levelno in {logging.DEBUG, logging.INFO}:
            return False
        else:
            return True


class ErrorFilter(logging.Filter):
    def filter(self, log_record):
        if log_record.levelno in {logging.WARNING, logging.ERROR, logging.CRITICAL}:
            return False
        else:
            return True


DEFAULT_LEVEL = logging.DEBUG
# logger_config = os.path.join(os.getenv('BACKUP_TOOL_DIR', None), 'config', 'config_logger.yaml')

# This statement will work until 'tests' dir has the same parent as 'config' dir (parent 'backup_tool' dir)
logger_config = os.path.join(
    Path(__file__).parent,
    'config', 'config_logger.yaml')

# Open YAML config for logging
if os.path.exists(logger_config):
    with open(logger_config, 'rt') as f:
        try:
            config = yaml.load(f.read(), Loader=EnvVarLoader)
            logging.config.dictConfig(config)
        except Exception as e:
            print(f'Unable to load YAML config file for logging, setting log level to DEFAULT {e}')
            logging.basicConfig(level=DEFAULT_LEVEL)

else:
    logging.basicConfig(level=DEFAULT_LEVEL)
    print('Unable to find YAML config file for logging, setting log level to DEFAULT')

