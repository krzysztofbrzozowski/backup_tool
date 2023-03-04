"""
@author:    Krzysztof Brzozowski
@file:      logger
@time:      04/03/2023
@desc:      
"""
import logging.config
import yaml
import os
import re
import colorlog

# Added path loader to load environment variable from in YAML file
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)

with open(os.path.join(
        os.getenv('BACKUP_TOOL_DIR', None), 'config', 'config_logger.yaml'), 'r') as f:
    config = yaml.load(f.read(), Loader=EnvVarLoader)
    logging.config.dictConfig(config)

logger = logging.getLogger('main_logger')
